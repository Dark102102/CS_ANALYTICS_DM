import type {Metadata} from 'next';
import './globals.css';
import { Toaster } from "@/components/ui/toaster"

export const metadata: Metadata = {
  title: 'CS Analytics',
  description: 'Predicting Counter-Strike match outcomes using data analysis and machine learning.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="font-body antialiased bg-image-wrapper">
        <div className="bg-overlay relative min-h-screen">
          <div className="relative z-10">
            {children}
            <Toaster />
          </div>
        </div>
      </body>
    </html>
  );
}
