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
    { src: "https://i.postimg.cc/pT3YyLgH/02-round-wins-by-side.png", alt: "Round Wins by Side" },
    { src: "https://i.postimg.cc/k5L27G0p/03-map-distribution.png", alt: "Map Distribution" },
    { src: "https://i.postimg.cc/Gpd215P1/04-round-wins-by-map-and-side.png", alt: "Round Wins by Map and Side" },
    { src: "https://i.postimg.cc/k47tXhJt/05-ct-win-rate-vs-t-win-rate.png", alt: "CT Win Rate vs T Win Rate" },
    { src: "https://i.postimg.cc/tTW2p3J3/06-average-round-duration.png", alt: "Average Round Duration" },
    { src: "https://i.postimg.cc/hGv5XJgJ/07-pistol-round-win-rate.png", alt: "Pistol Round Win Rate" },
    { src: "https://i.postimg.cc/sXJ0zYjM/08-first-kill-win-rate.png", alt: "First Kill Win Rate" },
    { src: "https://i.postimg.cc/vBQLG1hG/09-bomb-plant-win-rate.png", alt: "Bomb Plant Win Rate" },
    { src: "https://i.postimg.cc/J0c0mN2H/10-clutch-success-rate.png", alt: "Clutch Success Rate" },
    { src: "https://i.postimg.cc/Kz43xG9c/11-player-rating-distribution.png", alt: "Player Rating Distribution" },
    { src: "https://i.postimg.cc/pr0vMWhh/12-k-d-ratio-distribution.png", alt: "K/D Ratio Distribution" },
    { src: "https://i.postimg.cc/HxbYJgV1/13-team-rating-correlation.png", alt: "Team Rating Correlation" },
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
              <CardContent>
                 <Carousel className="w-full max-w-4xl mx-auto" opts={{ loop: true }}>
                  <CarouselContent>
                    {visualizations.map((vis, index) => (
                      <CarouselItem key={index}>
                        <div className="relative aspect-video">
                          <Image
                            src={vis.src}
                            alt={vis.alt}
                            fill
                            className="object-contain rounded-lg"
                          />
                        </div>
                         <p className="text-center text-white/70 mt-2">{index + 1}. {vis.alt}</p>
                      </CarouselItem>
                    ))}
                  </CarouselContent>
                  <CarouselPrevious className="ml-12" />
                  <CarouselNext className="mr-12" />
                </Carousel>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
