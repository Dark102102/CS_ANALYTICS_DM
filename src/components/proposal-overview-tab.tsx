import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CheckCircle2 } from 'lucide-react';

const sections = [
  {
    title: 'Research Topic',
    points: ['Counter-Strike match outcome prediction.'],
  },
  {
    title: 'Scope',
    points: ['Analyze historical match data, player stats, and team performance.'],
  },
  {
    title: 'Research Questions',
    points: [
      'Can we predict match winners with high accuracy?',
      'Which player/team stats have the biggest impact on outcomes?',
      'How can predictions support esports analytics?',
    ],
  },
];

export function ProposalOverviewTab() {
  return (
    <Card className="shadow-sm">
      <CardHeader>
        <CardTitle className="text-3xl font-bold text-primary">Proposal Overview</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {sections.map((section) => (
          <div key={section.title}>
            <h3 className="text-xl font-semibold mb-3">{section.title}</h3>
            <ul className="space-y-2 pl-2">
              {section.points.map((point) => (
                <li key={point} className="flex items-start gap-3">
                  <CheckCircle2 className="h-5 w-5 text-accent mt-1 flex-shrink-0" />
                  <span className="text-foreground/80">{point}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
