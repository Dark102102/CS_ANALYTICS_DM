import React from 'react';
import { Gamepad2 } from 'lucide-react';

export function Header({ children }: { children?: React.ReactNode }) {
  return (
    <header className="p-4 border-b border-white/10 bg-black/20 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Gamepad2 className="h-8 w-8 text-primary" />
          <h1 className="text-2xl font-bold tracking-tight text-white">
            CS Analytics
          </h1>
        </div>
        <nav>{children}</nav>
      </div>
    </header>
  );
}
