import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Target, Rocket, HelpCircle, Lightbulb, CheckCircle2 } from 'lucide-react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"

const researchTopic = {
  title: 'Research Topic',
  icon: <Target className="h-8 w-8 text-primary" />,
  description: 'Counter-Strike match outcome prediction using machine learning and statistical analysis of competitive gaming data.',
};

const projectScope = {
  title: 'Project Scope',
  icon: <Rocket className="h-8 w-8 text-green-400" />,
  points: [
    'Historical match data analysis spanning multiple tournaments',
    'Player performance statistics and individual skill metrics',
    'Team composition and strategic approach evaluation',
    'Map-specific performance patterns and preferences',
    'Real-time data integration for live match prediction',
  ],
};

const researchQuestions = {
  title: 'Proposed Research Questions (10)',
  icon: <HelpCircle className="h-8 w-8 text-purple-400" />,
  questions: [
      {
        title: '1. Pre-match Feature Correlation',
        text: 'What pre-match features (team Elo/ranking, recent form, map win rates, average player ratings) correlate most strongly with match winners in best-of-three professional CS2 matches?'
      },
      {
        title: '2. Player Statistics Impact',
        text: 'Which combination of player-level statistics (headshot %, entry kills, clutch success) maximizes predictive power for match outcome classification, as measured by feature importance in machine learning models?'
      },
      {
        title: '3. Round Winner Prediction',
        text: 'Can we predict round winners using only HLTV-derived per-round features (e.g., starting side, economy balances, weapons purchased) and recent team patterns? What is the best achievable accuracy with publicly-available features?'
      },
      {
        title: '4. 1v1 Duel Outcomes',
        text: 'How well can we predict 1v1 duel outcomes (player vs player) using player historical duel stats, weapon, and round context? Which features (weapon type, player KD, clutch history) are most predictive?'
      },
      {
        title: '5. Team Coordination Analysis',
        text: 'Do teams with higher measured coordination (proxied via multi-kill sequences, utility usage patterns, or consistent opening frag patterns) win more rounds on average than teams with higher raw frag counts but weaker coordination?'
      },
      {
        title: '6. Map Predictability',
        text: 'Are certain maps significantly more “predictable” than others (i.e., do models reach higher accuracy on some maps), and which map-specific features (T/CT side advantage, common bombsite control metrics) explain those differences?'
      },
      {
        title: '7. Market Information Integration',
        text: 'How quickly do pre-match betting markets incorporate new information (roster swaps, last-minute lineup changes), and can model-generated probabilities identify value bets that odds markets miss?'
      },
      {
        title: '8. Real-time Prediction Performance',
        text: 'Using only features that are plausibly available in near-real-time from public streams or HLTV updates, how well can a “lightweight” model predict round outcomes during a match, and what is its latency/throughput profile?'
      },
      {
        title: '9. Player Marginal Value',
        text: 'Which players provide the largest marginal increase in win probability when included in a team (measured via counterfactual / leave-one-out analyses), and how stable are those estimates across different time windows?'
      },
      {
        title: '10. Dataset Bias and Generalization',
        text: 'How sensitive are model predictions to dataset biases for example, when the dataset contains many matches from certain regions or event tiers and what de-biasing strategies (resampling, covariate adjustment) most improve generalization to unseen teams or regions?'
      },
  ]
};

const expectedOutcomes = {
  title: 'Expected Outcomes',
  icon: <Lightbulb className="h-8 w-8 text-orange-400" />,
  sections: [
    {
      title: 'Technical Deliverables',
      points: [
        'Prediction model with 85%+ accuracy',
        'Interactive analytics dashboard',
      ],
    },
    {
      title: 'Research Impact',
      points: [
        'Enhanced esports analytics',
        'Strategic insights for teams',
      ],
    },
  ],
};


export function ProposalOverviewTab() {
  const cardClassName = "shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border border-white/10 rounded-xl";
  const firstFiveQuestions = researchQuestions.questions.slice(0, 5);
  const nextFiveQuestions = researchQuestions.questions.slice(5, 10);
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
          Proposal <span className="text-primary">Overview</span>
        </h1>
        <p className="mt-4 text-lg leading-8 text-white/80 max-w-3xl mx-auto">
          A comprehensive research proposal outlining our approach to Counter-Strike match prediction through advanced analytics and machine learning.
        </p>
      </div>

      <div className="space-y-8 max-w-4xl mx-auto">
        {/* Research Topic */}
        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-primary/10 p-3 rounded-full">
              {researchTopic.icon}
            </div>
            <div>
              <CardTitle className="text-2xl text-white">{researchTopic.title}</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <p className="text-white/70 ml-16">{researchTopic.description}</p>
          </CardContent>
        </Card>

        {/* Project Scope */}
        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-green-400/10 p-3 rounded-full">
              {projectScope.icon}
            </div>
            <div>
              <CardTitle className="text-2xl text-white">{projectScope.title}</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="ml-16">
            <ul className="space-y-2">
              {projectScope.points.map((point) => (
                <li key={point} className="flex items-start gap-3">
                  <CheckCircle2 className="h-5 w-5 text-green-400 mt-1 flex-shrink-0" />
                  <span className="text-white/80">{point}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>

        {/* Research Questions */}
        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-purple-400/10 p-3 rounded-full">
              {researchQuestions.icon}
            </div>
            <div>
              <CardTitle className="text-2xl text-white">{researchQuestions.title}</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="ml-16">
            <Carousel className="w-full">
              <CarouselContent>
                <CarouselItem>
                  <div className="space-y-6">
                    {firstFiveQuestions.map(q => (
                       <div className="border-l-4 border-primary/50 pl-4" key={q.title}>
                        <h3 className="text-lg font-semibold text-white mb-2">{q.title}</h3>
                        <p className="text-white/80 leading-relaxed">{q.text}</p>
                      </div>
                    ))}
                  </div>
                </CarouselItem>
                 <CarouselItem>
                  <div className="space-y-6">
                    {nextFiveQuestions.map(q => (
                       <div className="border-l-4 border-primary/50 pl-4" key={q.title}>
                        <h3 className="text-lg font-semibold text-white mb-2">{q.title}</h3>
                        <p className="text-white/80 leading-relaxed">{q.text}</p>
                      </div>
                    ))}
                  </div>
                </CarouselItem>
              </CarouselContent>
              <CarouselPrevious className="ml-4" />
              <CarouselNext className="mr-4" />
            </Carousel>
          </CardContent>
        </Card>

        {/* Expected Outcomes */}
        <Card className={cardClassName}>
           <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-orange-400/10 p-3 rounded-full">
              {expectedOutcomes.icon}
            </div>
            <div>
              <CardTitle className="text-2xl text-white">{expectedOutcomes.title}</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="ml-16 grid md:grid-cols-2 gap-8">
            {expectedOutcomes.sections.map((section) => (
              <div key={section.title}>
                <h3 className="text-lg font-semibold mb-3 text-primary">{section.title}</h3>
                <ul className="space-y-2">
                  {section.points.map((point) => (
                    <li key={point} className="flex items-start gap-3">
                       <div className="w-1.5 h-1.5 bg-orange-400 rounded-full mt-2.5 flex-shrink-0"></div>
                      <span className="text-white/80">{point}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
