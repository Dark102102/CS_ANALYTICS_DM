import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Database, Filter, BarChart } from 'lucide-react';
import Image from 'next/image';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel"

const visualizations = [
    { src: "https://i.postimg.cc/9QfGQ7XC/01-round-wins-distribution.png", alt: "Round Wins Distribution" },
    { src: "https://i.postimg.cc/T3Pr3D2R/02-round-end-reasons.png", alt: "Round End Reasons" },
    { src: "https://i.postimg.cc/k40g5S0h/03-ct-vs-t-wins.png", alt: "CT vs T Wins" },
    { src: "https://i.postimg.cc/VLwzJt3L/04-map-win-percentages.png", alt: "Map Win Percentages" },
    { src: "https://i.postimg.cc/7ZpYtKJC/05-bomb-plant-defuse-rates.png", alt: "Bomb Plant & Defuse Rates" },
    { src: "https://i.postimg.cc/VvKgM74G/06-economy-vs-wins.png", alt: "Economy vs Wins" },
    { src: "https://i.postimg.cc/L8Qd1fFj/07-player-impact-distribution.png", alt: "Player Impact Distribution" },
    { src: "https://i.postimg.cc/zX8P0XhV/08-weapon-k-d-ratios.png", alt: "Weapon K/D Ratios" },
    { src: "https://i.postimg.cc/c12YJzFq/09-clutch-success-rates.png", alt: "Clutch Success Rates" },
    { src: "https://i.postimg.cc/bJqS2bN3/10-utility-damage-per-round.png", alt: "Utility Damage Per Round" },
    { src: "https://i.postimg.cc/mD8zQG8Y/11-first-kill-impact.png", alt: "First Kill Impact" },
    { src: "https://i.postimg.cc/44rGvj9g/12-team-form-over-time.png", alt: "Team Form Over Time" },
    { src: "https://i.postimg.cc/8c7TqWmM/13-betting-odds-vs-actual-outcome.png", alt: "Betting Odds vs Actual Outcome" },
];

export function DataExplorationTab() {
  const cardClassName = "shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border-white/10 rounded-xl min-h-[300px]";

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
          Data <span className="text-primary">Exploration</span>
        </h1>
        <p className="mt-4 text-lg leading-8 text-white/80 max-w-3xl mx-auto">
          This section details our process for collecting, cleaning, and visualizing the data used in our predictive models.
        </p>
      </div>

      <Tabs defaultValue="collection" className="w-full">
        <TabsList className="grid w-full grid-cols-3 max-w-2xl mx-auto bg-black/30 backdrop-blur-sm">
          <TabsTrigger value="collection">
            <Database className="w-4 h-4 mr-2" />
            Data Collection
          </TabsTrigger>
          <TabsTrigger value="preprocessing">
            <Filter className="w-4 h-4 mr-2" />
            Cleaning & Preprocessing
          </TabsTrigger>
          <TabsTrigger value="visualizations">
            <BarChart className="w-4 h-4 mr-2" />
            Visualizations
          </TabsTrigger>
        </TabsList>

        <div className="mt-8">
          <TabsContent value="collection">
            <Card className={cardClassName}>
              <CardHeader>
                <CardTitle className="text-2xl text-primary">Data Collection</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-white/80 leading-relaxed">
                  Placeholder for Data Collection. This section will describe the sources and methods used to gather raw data, such as scraping from HLTV, accessing betting odds APIs, and collecting player statistics. We will detail the scope of the data, including the time period covered, the number of matches, and the specific features collected for teams and players.
                </p>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="preprocessing">
            <Card className={cardClassName}>
              <CardHeader>
                <CardTitle className="text-2xl text-primary">Data Cleaning and Preprocessing</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-white/80 leading-relaxed">
                  Placeholder for Data Cleaning and Preprocessing. Here, we will outline the steps taken to clean the raw data, including handling missing values, correcting inconsistencies, and normalizing data formats. This section will also cover feature engineering, where we create new predictive features from the base data, such as team form, map-specific strengths, and economic advantages.
                </p>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="visualizations">
            <Card className={cardClassName}>
              <CardHeader>
                <CardTitle className="text-2xl text-primary">Visualizations</CardTitle>
              </CardHeader>
              <CardContent className="flex items-center justify-center">
                 <Carousel className="w-full max-w-2xl" opts={{ loop: true }}>
                  <CarouselContent>
                    {visualizations.map((vis, index) => (
                      <CarouselItem key={index}>
                        <div className="p-1">
                            <div className="relative aspect-video">
                                <Image
                                    src={vis.src}
                                    alt={vis.alt}
                                    fill
                                    className="object-contain rounded-lg"
                                />
                            </div>
                            <p className="text-center text-white/70 mt-2">{vis.alt}</p>
                        </div>
                      </CarouselItem>
                    ))}
                  </CarouselContent>
                  <CarouselPrevious className="ml-12 text-white" />
                  <CarouselNext className="mr-12 text-white" />
                </Carousel>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
