from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os
import uuid
import logging
import stat
from pathlib import Path
from typing import List
from app.dependencies import get_current_user

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter()

# 创建上传目录
UPLOAD_DIR = Path("uploads")
try:
    UPLOAD_DIR.mkdir(exist_ok=True)
    # 确保目录有写权限
    os.chmod(UPLOAD_DIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
except Exception as e:
    logger.error(f"创建上传目录失败: {str(e)}")

# 允许的文件扩展名
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "wmv"}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_VIDEO_EXTENSIONS)

# 最大文件大小 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/upload", summary="上传文件")
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """
    上传图片或视频文件
    
    - **file**: 要上传的文件
    - 返回上传成功的文件信息，包括文件名和访问URL
    """
    try:
        logger.info(f"用户 {current_user.id} 开始上传文件: {file.filename}")
        
        # 检查文件扩展名
        file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型，只支持: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # 读取文件内容
        contents = await file.read()
        
        # 检查文件大小
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="文件大小超过限制（10MB）"
            )
        
        # 重置文件指针，因为我们已经读取过一次
        await file.seek(0)

        # 生成唯一文件名
        file_uuid = str(uuid.uuid4())
        filename = f"{file_uuid}.{file_ext}"
        file_path = UPLOAD_DIR / filename
        
        # 确保上传目录存在并有写权限
        try:
            UPLOAD_DIR.mkdir(exist_ok=True)
            os.chmod(UPLOAD_DIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except Exception as e:
            logger.error(f"确保上传目录存在时出错: {str(e)}")

        logger.info(f"保存文件到: {file_path}")

        # 保存文件
        try:
            with open(file_path, "wb") as f:
                while chunk := await file.read(1024 * 1024):  # 逐块读取以节省内存
                    f.write(chunk)
            # 设置文件权限
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        except PermissionError as pe:
            logger.error(f"权限错误: {str(pe)}")
            raise HTTPException(
                status_code=500,
                detail=f"没有权限写入文件: {str(pe)}"
            )
        except Exception as e:
            logger.error(f"保存文件时出错: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"保存文件失败: {str(e)}"
            )

        # 确定文件类型
        file_type = "image" if file_ext in ALLOWED_IMAGE_EXTENSIONS else "video"
        
        logger.info(f"文件上传成功: {filename}")
        
        return {
            "code": 200,
            "message": "上传成功",
            "data": {
                "filename": filename,
                "url": f"/api/v1/files/{filename}",
                "type": file_type
            }
        }
    except HTTPException as he:
        logger.error(f"HTTP错误: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"文件上传过程中发生错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"文件上传失败: {str(e)}"
        )

@router.get("/{filename}", summary="获取文件")
async def get_file(filename: str):
    """
    获取上传的文件
    
    - **filename**: 文件名
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(file_path)

@router.delete("/{filename}", summary="删除文件")
async def delete_file(
    filename: str,
    current_user = Depends(get_current_user)
):
    """
    删除上传的文件
    
    - **filename**: 文件名
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    try:
        os.remove(file_path)
        return {
            "code": 200,
            "message": "文件删除成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")