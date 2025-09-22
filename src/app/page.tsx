import { Header } from '@/components/header';
import { IntroductionTab } from '@/components/introduction-tab';
import { TeamTab } from '@/components/team-tab';
import { ProposalOverviewTab } from '@/components/proposal-overview-tab';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function Home() {
  return (
    <div className="min-h-screen">
      <Tabs defaultValue="introduction" className="w-full">
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
  );
}
