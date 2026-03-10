import { expect, test } from '@playwright/test';

test('desktop smoke flow: launch -> setup -> ask -> answer', async ({ page }) => {
  const appUrl = process.env.E2E_APP_URL ?? 'http://localhost:4173';

  await page.goto(appUrl);

  await page.getByLabel('Backend URL').fill('http://localhost:8787');
  await page.getByLabel('API Key').fill('test-api-key');
  await page.getByRole('button', { name: 'Save Settings' }).click();

  await page.getByPlaceholder('Ask a question').fill('RAG 동작을 요약해줘');
  await page.getByRole('button', { name: 'Send' }).click();

  await expect(page.getByTestId('assistant-message').last()).toBeVisible();
});
