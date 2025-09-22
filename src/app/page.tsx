import { Header } from '@/components/header';
import { IntroductionTab } from '@/components/introduction-tab';
import { TeamTab } from '@/components/team-tab';
import { ProposalOverviewTab } from '@/components/proposal-overview-tab';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto p-4 md:p-8">
        <Tabs defaultValue="team" className="w-full">
          <div className="flex justify-center">
            <TabsList className="grid w-full grid-cols-1 sm:grid-cols-3 md:w-auto mb-8">
                <TabsTrigger value="introduction">Introduction</TabsTrigger>
                <TabsTrigger value="team">Team</TabsTrigger>
                <TabsTrigger value="proposal">Proposal Overview</TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value="introduction">
            <IntroductionTab />
          </TabsContent>
          <TabsContent value="team">
            <TeamTab />
          </TabsContent>
          <TabsContent value="proposal">
            <ProposalOverviewTab />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
