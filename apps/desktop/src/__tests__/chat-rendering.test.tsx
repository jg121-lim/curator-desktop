import React from 'react';
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';

type Message = { role: 'user' | 'assistant'; content: string };

function ChatTranscript({ messages }: { messages: Message[] }) {
  return (
    <section>
      {messages.map((m, i) => (
        <article key={`${m.role}-${i}`} data-testid={`message-${i}`}>
          <strong>{m.role}:</strong> {m.content}
        </article>
      ))}
    </section>
  );
}

describe('chat rendering', () => {
  it('renders both user and assistant messages in order', () => {
    render(
      <ChatTranscript
        messages={[
          { role: 'user', content: '첫 질문' },
          { role: 'assistant', content: '첫 응답' },
        ]}
      />,
    );

    const first = screen.getByTestId('message-0');
    const second = screen.getByTestId('message-1');

    expect(first.textContent).toContain('user:');
    expect(first.textContent).toContain('첫 질문');
    expect(second.textContent).toContain('assistant:');
    expect(second.textContent).toContain('첫 응답');
  });
});
