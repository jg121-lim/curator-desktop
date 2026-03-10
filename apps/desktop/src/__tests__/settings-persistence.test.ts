import { describe, expect, it } from 'vitest';

type AppSettings = {
  baseUrl: string;
  apiKey: string;
  confluenceSpace: string;
};

const SETTINGS_KEY = 'curator.settings';

function saveSettings(settings: AppSettings, storage: Storage) {
  storage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

function loadSettings(storage: Storage): AppSettings | null {
  const raw = storage.getItem(SETTINGS_KEY);
  if (!raw) return null;
  return JSON.parse(raw) as AppSettings;
}

describe('settings persistence', () => {
  it('saves and restores settings from localStorage', () => {
    const settings: AppSettings = {
      baseUrl: 'http://localhost:8787',
      apiKey: 'secret',
      confluenceSpace: 'ENG',
    };

    saveSettings(settings, window.localStorage);
    const loaded = loadSettings(window.localStorage);

    expect(loaded).toEqual(settings);
  });
});
