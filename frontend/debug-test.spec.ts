import { test } from '@playwright/test';

test('debug navigation', async ({ page }) => {
  await page.goto('http://localhost:80/login');
  await page.fill('input[placeholder*="username"]', 'e2e1_309895');
  await page.fill('input[type="password"]', 'Pass123');
  await page.getByRole('button', { name: /Login/i }).click();
  await page.waitForURL(/.*home/, { timeout: 10000 });
  await page.waitForLoadState('networkidle');
  
  console.log('Current URL:', page.url());
  
  // Print all menu items
  const menuItems = await page.locator('.el-menu-item').all();
  for (const item of menuItems) {
    const text = await item.textContent();
    console.log('Menu item:', text);
  }
  
  // Try clicking
  await page.locator('.el-menu-item').filter({ hasText: 'My Needs' }).click();
  await page.waitForTimeout(3000);
  console.log('After click URL:', page.url());
});
