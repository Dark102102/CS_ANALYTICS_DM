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
            <CardTitle className="text-2xl text-white">Key Findings</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4 list-disc list-inside text-white/80 ml-16">
              <li>
                <span className="font-semibold text-white">CT rounds are won by better shooting.</span>
                <p className="pl-6 text-white/70">When CTs deal more damage, secure more kills, and land more headshots, they win a much higher share of rounds.</p>
              </li>
              <li>
                <span className="font-semibold text-white">T rounds are won by taking the right fights.</span>
                <p className="pl-6 text-white/70">Terrorists succeed when they force favorable duels: longer-range engagements, smart wallbangs, and strong positional play all raise their win rate.</p>
              </li>
              <li>
                <span className="font-semibold text-white">Two main player archetypes emerge.</span>
                <p className="pl-6 text-white/70">Our clustering shows Entry Fraggers (very aggressive, get early kills but also die early) and Closer/Support Players (slower, more stable players who survive longer and often finish rounds).</p>
              </li>
              <li>
                <span className="font-semibold text-white">Economy is the strongest single predictor of round outcome.</span>
                <p className="pl-6 text-white/70">The feature that predicted the round winner best was the economic difference between teams. A team with a stronger buy has a clear statistical advantage.</p>
              </li>
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
             <ul className="space-y-4 list-disc list-inside text-white/80 ml-16">
                <li>
                  <span className="font-semibold text-white">Better practice planning for esports teams.</span>
                  <p className="pl-6 text-white/70">Coaches can design drills targeting CT aim consistency, T-side positioning, and role-specific training based on player tendencies.</p>
                </li>
                <li>
                  <span className="font-semibold text-white">Deeper understanding of maps and game economics.</span>
                  <p className="pl-6 text-white/70">Our results highlight which situations are most favorable on a map and how much economic advantage is “enough” to expect a win.</p>
                </li>
                <li>
                  <span className="font-semibold text-white">Smarter buy/save decisions.</span>
                  <p className="pl-6 text-white/70">Teams can estimate their disadvantage in a given round and use that signal to decide whether to full buy, half buy, or save for a stronger future round.</p>
                </li>
              </ul>
          </CardContent>
        </Card>

        <Card className={cardClassName}>
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex-shrink-0 bg-orange-400/10 p-3 rounded-full">
              <AlertTriangle className="h-8 w-8 text-orange-400" />
            </div>
            <CardTitle className="text-2xl text-white">Future Work</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-4 list-disc list-inside text-white/80 ml-16">
              <li>
                <span className="font-semibold text-white">Apply the approach to other esports</span> like Valorant, League of Legends, Dota 2, and StarCraft II.
              </li>
              <li>
                <span className="font-semibold text-white">Incorporate richer feature sets</span> (utility usage, heatmaps, communication) to improve prediction accuracy.
              </li>
              <li>
                <span className="font-semibold text-white">Develop real-time prediction models</span> for live coaching and automated tournament analysis.
              </li>
               <li>
                <span className="font-semibold text-white">Explore reinforcement learning</span> to capture micro and macro decision-making processes.
              </li>
              <li>
                <span className="font-semibold text-white">Investigate cross-domain strategy transfer</span> to apply learnings to other games or even non-gaming domains.
              </li>
               <li>
                <span className="font-semibold text-white">Improve long-horizon memory and retrieval</span> for games requiring long sequences of decisions.
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
