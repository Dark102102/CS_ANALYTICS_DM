'use client';
import { useState } from 'react';
import { Header } from '@/components/header';
import { IntroductionTab } from '@/components/introduction-tab';
import { TeamTab } from '@/components/team-tab';
import { ProposalOverviewTab } from '@/components/proposal-overview-tab';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { cn } from '@/lib/utils';

export default function Home() {
  const [activeTab, setActiveTab] = useState('introduction');

  const backgroundClass = () => {
    switch (activeTab) {
      case 'proposal':
        return 'bg-image-proposal';
      case 'team':
        return 'bg-image-team';
      default:
        return 'bg-image-default';
    }
  };

  return (
    <div className={cn(
        "min-h-screen transition-background-image",
        backgroundClass()
      )}>
      <div className="bg-overlay relative min-h-screen">
        <div className="relative z-10">
          <Tabs defaultValue="introduction" className="w-full" onValueChange={setActiveTab}>
            <Header>
              <TabsList className="grid w-full grid-cols-1 sm:grid-cols-3 md:w-auto bg-transparent border-0 p-0">
                <TabsTrigger value="introduction" className="text-lg">Introduction</TabsTrigger>
                <TabsTrigger value="team" className="text-lg">Team</TabsTrigger>
                <TabsTrigger value="proposal" className="text-lg">Proposal Overview</TabsTrigger>
              </TabsList>
            </Header>
            <main className="container mx-auto p-4 md:p-8">
              <TabsContent value="introduction">
                <IntroductionTab />
              </TabsContent>
              <TabsContent value="team">
                <TeamTab />
              </TabsContent>
              <TabsContent value="proposal">
                <ProposalOverviewTab />
              </TabsContent>
            </main>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
