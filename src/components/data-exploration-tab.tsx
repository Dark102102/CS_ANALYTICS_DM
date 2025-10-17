import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Database, Filter, BarChartHorizontal } from 'lucide-react';
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from 'recharts';

const sampleData = [
  { map: 'Dust 2', teamA: 13, teamB: 8 },
  { map: 'Mirage', teamA: 16, teamB: 12 },
  { map: 'Inferno', teamA: 10, teamB: 13 },
  { map: 'Nuke', teamA: 7, teamB: 13 },
  { map: 'Overpass', teamA: 13, teamB: 5 },
  { map: 'Vertigo', teamA: 9, teamB: 13 },
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
              <CardContent className="h-[400px]">
                <p className="text-white/80 leading-relaxed mb-4">
                  This area will showcase a variety of interactive charts and graphs to explore the dataset. Below is an example of an interactive chart built with Recharts, which can be powered by data exported from Python.
                </p>
                <ResponsiveContainer width="100%" height="90%">
                  <BarChart data={sampleData} layout="vertical" margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <XAxis type="number" stroke="hsl(var(--foreground))" opacity={0.8} />
                    <YAxis dataKey="map" type="category" stroke="hsl(var(--foreground))" opacity={0.8} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: 'hsl(var(--background))',
                        borderColor: 'hsl(var(--border))',
                      }}
                      labelStyle={{ color: 'hsl(var(--primary))' }}
                    />
                    <Legend wrapperStyle={{ color: 'hsl(var(--foreground))', opacity: 0.8 }} />
                    <Bar dataKey="teamA" fill="hsl(var(--chart-1))" name="Team A Wins" />
                    <Bar dataKey="teamB" fill="hsl(var(--chart-2))" name="Team B Wins" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
