import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Database, Filter, BarChartHorizontal } from 'lucide-react';
import Image from 'next/image';

const visualizationImages = [
  { src: 'https://i.postimg.cc/k1h49QT/figure.png', alt: 'Feature Importance for Match Winner' },
  { src: 'https://i.postimg.cc/sK0W1Pq/figure-1.png', alt: 'Feature Importance for Round Winner' },
  { src: 'https://i.postimg.cc/z5pBJWg/figure-2.png', alt: 'Player Rating Distribution' },
  { src: 'https://i.postimg.cc/L5T88P0/figure-3.png', alt: 'Headshot Percentage Distribution' },
  { src: 'https://i.postimg.cc/HhCg834/figure-4.png', alt: 'Map Play Frequency' },
  { src: 'https://i.postimg.cc/PggH4w1/figure-5.png', alt: 'T-side Win Percentage by Map' },
  { src: 'https://i.postimg.cc/VMyLhMB/figure-6.png', alt: 'CT-side Win Percentage by Map' },
  { src: 'https://i.postimg.cc/pwnsR8r/figure-7.png', alt: 'Average Rounds per Match' },
  { src: 'https://i.postimg.cc/sVq1TfT/figure-8.png', alt: 'Elo vs. Average Player Rating' },
  { src: 'https://i.postimg.cc/f8L1Lg2/figure-9.png', alt: 'Opening Kill Success Rate by Team' },
  { src: 'https://i.postimg.cc/Jj6g0V6/figure-10.png', alt: 'Clutch Success Rate by Player' },
  { src: 'https://i.postimg.cc/q1zYJb2/figure-11.png', alt: 'Correlation Matrix of Player Stats' },
  { src: 'https://i.postimg.cc/0Vfc2K1/figure-12.png', alt: 'Team Economy Management' },
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
            <BarChartHorizontal className="w-4 h-4 mr-2" />
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
                <p className="text-white/80 leading-relaxed mb-6">
                  This section showcases a variety of visualizations generated from our dataset, providing insights into match dynamics, player performance, and map statistics. These plots are exported from our Python analysis scripts.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {visualizationImages.map((image, index) => (
                    <div key={index} className="rounded-lg overflow-hidden border-2 border-white/10 shadow-lg transition-transform hover:scale-105">
                       <Image
                        src={image.src}
                        alt={image.alt}
                        width={600}
                        height={400}
                        className="w-full h-auto object-contain"
                        data-ai-hint="chart graph"
                      />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
