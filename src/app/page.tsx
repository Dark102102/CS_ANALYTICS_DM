import { Header } from '@/components/header';
import { IntroductionTab } from '@/components/introduction-tab';
import { TeamTab } from '@/components/team-tab';
import { ProposalOverviewTab } from '@/components/proposal-overview-tab';
import { EsportsInsightGenerator } from '@/components/esports-insight-generator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto p-4 md:p-8">
        <Tabs defaultValue="team" className="w-full">
          <div className="flex justify-center">
            <TabsList className="grid w-full grid-cols-2 sm:grid-cols-4 md:w-auto mb-8">
                <TabsTrigger value="introduction">Introduction</TabsTrigger>
                <TabsTrigger value="team">Team</TabsTrigger>
                <TabsTrigger value="proposal">Proposal Overview</TabsTrigger>
                <TabsTrigger value="insights">AI Insights</TabsTrigger>
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
          <TabsContent value="insights">
            <EsportsInsightGenerator />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
