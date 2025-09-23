import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, BrainCircuit, Code } from 'lucide-react';
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
import { Button } from '@/components/ui/button';
import { useState } from 'react';
import { ChevronsUpDown } from 'lucide-react';

const features = [
  {
    icon: <BarChart className="h-8 w-8 text-primary" />,
    title: 'Data Analysis',
    description: 'Comprehensive analysis of historical match data, player statistics, and team performance metrics to identify winning patterns.',
  },
  {
    icon: <Code className="h-8 w-8 text-primary" />,
    title: 'Machine Learning',
    description: 'Advanced ML algorithms to predict match outcomes with high accuracy, providing valuable insights for competitive gaming.',
  },
  {
    icon: <BrainCircuit className="h-8 w-8 text-primary" />,
    title: 'Esports Analytics',
    description: 'Supporting the growing esports industry with data-driven insights and predictive analytics for better strategic decisions.',
  },
];

export function IntroductionTab() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <div className="space-y-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
          <span className="text-primary">Counter-Strike</span> Match Prediction
        </h1>
        <p className="mt-6 text-lg leading-8 text-white/80 max-w-2xl mx-auto">
          This project focuses on predicting the outcomes of Counter-Strike matches using data analysis and machine learning techniques. The goal is to understand patterns, improve prediction accuracy, and provide insights into competitive gaming.
        </p>
      </div>

      <div className="max-w-4xl mx-auto space-y-6">
        <div className="rounded-xl bg-black/30 backdrop-blur-sm p-8 border border-white/10">
          <Collapsible open={isOpen} onOpenChange={setIsOpen}>
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold mb-4 text-primary">Project Overview</h2>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm" className="w-9 p-0">
                  <ChevronsUpDown className="h-4 w-4" />
                  <span className="sr-only">Toggle</span>
                </Button>
              </CollapsibleTrigger>
            </div>
            <p className="text-white/80 leading-relaxed mb-6">
              This project investigates outcome prediction and strategic insight in Counter-Strike 2 (CS2) by analyzing HLTV and betting-odds data. Our goal is to develop accurate, lightweight, and accessible predictive models and analytical tools for players, teams, analysts, and fans. We will assemble a comprehensive dataset, conduct descriptive analyses, build predictive models for match and round outcomes, and create an interactive dashboard to make these insights actionable. By bridging the gap between academic research and practical application, this work aims to enrich the CS2 community with data-driven strategies and a deeper understanding of the game.
            </p>
            <CollapsibleContent>
              <p className="text-white/80 leading-relaxed mb-6">
                The implications of improved predictive and analytical tools for CS2 are wide: professional esports organizations can use model outputs to inform practice schedules, draft decisions, and in-match coaching adjustments; individual players can identify weaknesses in their play or tendencies that opponents exploit; broadcast teams can present more meaningful statistics and probabilistic storylines; and betting operators or data-driven tipsters can use model outputs to refine odds and identify value bets. Beyond direct esports actors, game developers and map designers may benefit from aggregated insights that reveal balance issues or tactical imbalances on certain maps. Academic researchers in sports analytics and real-time sequential prediction can use CS2 as a complex testbed for novel models (for example, real-time survival/prediction models for in-round events). There are also societal and regulatory stakeholders to consider: as betting becomes more prominent in esports, research that clarifies model reliability and limitations can inform consumer protection and responsible-gambling efforts. Finally, the broader gaming community would gain tools and accessibility if we can produce clear, actionable dashboards for smaller teams and hobby players. Several existing platforms and vendors already supply analytics and odds comparison, so our project will need to show how it complements or improves upon those offerings.
              </p>
              <p className="text-white/80 leading-relaxed mb-6">
                There is a growing literature and industry practice around esports prediction and analytics. Academic and practitioner work ranges from logistic-regression and tree-based models that predict match outcomes from historical stats to deep sequential models that attempt in-game, real-time micro-predictions (for example, predicting player deaths or next-event probabilities). Projects such as "Predicting Round and Game Winners in CSGO" and conference work on real-time in-game death prediction have shown that machine learning can outperform naive baselines, especially when in-round state and equipment data are included. Industry teams (e.g., PandaScore, various odds aggregators) have written about modeling round dynamics and the need to treat the round as a whole dynamic process rather than a set of independent predictions. However, gaps remain: (1) many academic works focus on CS:GO demos or controlled datasets that are not straightforwardly accessible to casual practitioners; (2) real-time models often require telemetry that's unavailable outside tournament infrastructure, limiting applicability; and (3) few works combine betting-odds features and traditional match statistics in the same predictive pipeline to quantify how much market information already encodes. Another notable practical gap is user accessibility — sophisticated models frequently lack clear interpretation or simple interfaces that hobbyist players can use. Our project explicitly targets these gaps by using publicly accessible HLTV data (scraped) and betting-odds feeds to produce models that prioritize both predictive performance and interpretability/accessibility for non-enterprise users.
              </p>
              <p className="text-white/80 leading-relaxed mb-6">
                At a high level, our project will: (1) assemble and clean a combined dataset drawn from HLTV scrapes (match histories, player stats, team maps, map scores), per-match and per-round features when available, and betting-odds snapshots (pre-match and — when possible — intra-event odds); (2) design descriptive analyses and visualizations that surface common strategic patterns (economy swings, common utility usage patterns at pro levels, map-specific win biases); (3) construct and evaluate predictive models at multiple granularities: round winner, match winner, player duel (1v1) outcomes, and key in-round events (early picks, clutches); (4) emphasize model interpretability and lightweight real-time variants that can run with data available via HLTV and public feeds; and (5) create a model that can predict outcomes given the state of a game. Potential datasets and sources include scraped HLTV match and player pages, aggregated map statistics from HLTV, odds and market data from odds-comparison APIs and historical odds archives. The project will compare baseline models (logistic regression, random forest) with more complex sequential/time-aware models (LSTM/GRU or temporal XGBoost features) and will place a strong emphasis on cross-validation strategies that respect time ordering. We will prioritize prediction tasks but still include descriptive analyses that make the results actionable for players and analysts.
              </p>
              <p className="text-white/80 leading-relaxed">
                This project is designed to deliver predictive and analytical tools that are both accurate and accessible. By integrating HLTV match statistics with betting-odds data, we will produce interpretable models that forecast outcomes at multiple granularities (rounds, matches, duels, in-round events) while surfacing strategic insights that players, teams, and analysts can act on. The outcome will not only be research-grade evaluations of predictive models but also practical outputs: visual dashboards that highlight team strategies and tendencies, lightweight models suitable for near-real-time prediction, and interpretable metrics that make advanced analytics usable for non-enterprise audiences. Ultimately, our work aims to bridge the gap between academic esports research and practical applications, creating a foundation that improves team decision-making, enriches broadcasts, informs betting markets, and provides accessible tools for the broader Counter-Strike community.
              </p>
            </CollapsibleContent>
          </Collapsible>
        </div>

        <div className="rounded-xl bg-black/30 backdrop-blur-sm p-8 border border-white/10">
          <h2 className="text-2xl font-bold mb-4 text-primary">Citations</h2>
          <div className="space-y-4">
            <div className="border-l-4 border-primary/30 pl-4">
              <p className="text-white/80 leading-relaxed">
                Rubin, A. (2022). Predicting Round and Game Winners in CSGO. OSF Preprints. <a href="https://osf.io/preprints/u9j5g/" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80 underline">https://osf.io/preprints/u9j5g/</a>
              </p>
            </div>

            <div className="border-l-4 border-primary/30 pl-4">
              <p className="text-white/80 leading-relaxed">
                Marshall, S., Mavromoustakos Blom, P., & Spronck, P. (2022). Enabling Real-Time Prediction of In-game Deaths through Telemetry in Counter-Strike: Global Offensive. Paper presented at FDG22: 17th International Conference on the Foundations of Digital Games, Athens, Greece. <a href="https://doi.org/10.1145/3555858.3555859" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80 underline">https://doi.org/10.1145/3555858.3555859</a>
              </p>
            </div>

            <div className="border-l-4 border-primary/30 pl-4">
              <p className="text-white/80 leading-relaxed">
                Björklund, A., Lindevall, F., Svensson, P., & Johansson Visuri, W. (2018). Predicting the outcome of CS:GO games using machine learning. Bachelor's thesis, Chalmers University of Technology. Available at: <a href="https://publications.lib.chalmers.se/records/fulltext/256129/256129.pdf" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80 underline">https://publications.lib.chalmers.se/records/fulltext/256129/256129.pdf</a>
              </p>
            </div>

            <div className="border-l-4 border-primary/30 pl-4">
              <p className="text-white/80 leading-relaxed">
                Xenopoulos, P., Coelho, B., & Silva, C. (2021). Optimal Team Economic Decisions in Counter-Strike. arXiv preprint arXiv:2109.12990. <a href="https://arxiv.org/abs/2109.12990" target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80 underline">https://arxiv.org/abs/2109.12990</a>
              </p>
            </div>
          </div>
        </div>

      </div>

      <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title} className="text-center shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border-white/10 rounded-xl">
            <CardHeader>
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 mb-4">
                {feature.icon}
              </div>
              <CardTitle className="text-white">{feature.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-white/70">{feature.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="rounded-xl bg-black/30 backdrop-blur-sm p-8 border border-white/10">
        <h2 className="text-2xl font-bold text-center mb-4 text-primary">Project Impact</h2>
        <p className="text-white/80 text-center max-w-3xl mx-auto">
          By leveraging machine learning and statistical analysis, this project aims to revolutionize how we understand competitive Counter-Strike, providing valuable insights for players, teams, and analysts in the esports ecosystem.
        </p>
      </div>
    </div>
  );
}
