import React from 'react';
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';

function ConnectionStatus({ connected }: { connected: boolean }) {
  if (connected) return <p>서버 연결됨</p>;
  return (
    <div role="alert">
      <h2>연결 실패</h2>
      <p>백엔드에 연결할 수 없습니다. 설정을 확인해 주세요.</p>
      <button>다시 시도</button>
    </div>
  );
}

describe('connection failure UI', () => {
  it('shows an alert and retry button when backend connection fails', () => {
    render(<ConnectionStatus connected={false} />);

    expect(screen.getByRole('alert')).toBeTruthy();
    expect(screen.getByText('연결 실패')).toBeTruthy();
    expect(screen.getByRole('button', { name: '다시 시도' })).toBeTruthy();
  });
});
