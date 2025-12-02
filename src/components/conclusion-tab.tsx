import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Lightbulb, Search, TrendingUp, AlertTriangle } from 'lucide-react';

export function ConclusionTab() {
  const cardClassName = "shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border-white/10 rounded-xl";

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
          Conclusion & <span className="text-primary">Results</span>
        </h1>
        <p className="mt-4 text-lg leading-8 text-white/80 max-w-3xl mx-auto">
          A summary of our findings, their impact, and the future direction of this project.
        </p>
      </div>

      <div className="space-y-6 max-w-4xl mx-auto">
        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-primary/10 p-3 rounded-full">
              <Lightbulb className="h-8 w-8 text-primary" />
            </div>
            <CardTitle className="text-2xl text-white">Non-Technical Summary</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-white/80 leading-relaxed ml-16">
              Our project successfully demonstrated that we can predict Counter-Strike 2 match outcomes with high accuracy by analyzing game data. We discovered that key factors like player accuracy, economic management, and objective control (like planting or defusing the bomb) are strong indicators of which team will win a round. We also identified distinct player roles—aggressive "Entry Fraggers" and supportive "Balanced Players"—based on their in-game actions, showing that team composition is crucial for success.
            </p>
          </CardContent>
        </Card>

        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-purple-400/10 p-3 rounded-full">
              <Search className="h-8 w-8 text-purple-400" />
            </div>
            <CardTitle className="text-2xl text-white">Key Insights & Discoveries</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-3 list-disc list-inside text-white/80 ml-16">
              <li>Terrorist-side wins are strongly linked to high headshot rates combined with successful bomb plants.</li>
              <li>Counter-Terrorist victories depend more on objective control and defusing the bomb than on sheer mechanical skill.</li>
              <li>Player performance, measured by damage dealt per round, is highly predictable from core combat stats like kills and deaths.</li>
              <li>Machine learning models, particularly Random Forests, can achieve near-perfect accuracy in predicting round winners based on our dataset.</li>
            </ul>
          </CardContent>
        </Card>

        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-green-400/10 p-3 rounded-full">
              <TrendingUp className="h-8 w-8 text-green-400" />
            </div>
            <CardTitle className="text-2xl text-white">Real-World Impact</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-white/80 leading-relaxed ml-16">
              These results can have a significant impact on the esports community. Professional teams can use these insights to refine strategies and scout players with specific profiles. Analysts and broadcast commentators can provide deeper, data-driven narratives during live matches. For the wider gaming community, our work provides a clearer understanding of what it takes to win at a high level.
            </p>
          </CardContent>
        </Card>

        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-orange-400/10 p-3 rounded-full">
              <AlertTriangle className="h-8 w-8 text-orange-400" />
            </div>
            <CardTitle className="text-2xl text-white">Limitations & Future Work</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-white/80 leading-relaxed ml-16">
              Our analysis was based on a specific set of professional matches, so the models may need to be validated on a larger, more diverse dataset. The perfect scores from some models suggest potential data leakage or the need for more complex, out-of-sample testing.
            </p>
            <p className="text-white/80 leading-relaxed mt-4 ml-16">
              Future work could involve incorporating real-time data for live predictions, analyzing communication patterns, and expanding the models to include a wider range of competitive tiers to see how strategies differ.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
