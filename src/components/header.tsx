import { Gamepad2 } from 'lucide-react';

export function Header() {
  return (
    <header className="p-4 border-b bg-card">
      <div className="container mx-auto flex items-center gap-4">
        <Gamepad2 className="h-8 w-8 text-primary" />
        <h1 className="text-2xl font-bold tracking-tight text-foreground">
          CS Analytics
        </h1>
      </div>
    </header>
  );
}
