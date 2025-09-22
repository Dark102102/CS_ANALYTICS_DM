import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, BrainCircuit, Code } from 'lucide-react';

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
