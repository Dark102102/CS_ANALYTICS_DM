
'use client';
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Database, Filter, BarChart } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import Image from 'next/image';

const visualizations = Array.from({ length: 13 }).map((_, i) => {
  if (i === 0) {
    return {
      id: `viz-1`,
      title: `Round Wins by Side`,
      imageUrl: `https://i.postimg.cc/9QfGQ7XC/01-round-wins-distribution.png`,
      description: `A bar chart showing the distribution of round wins for the Terrorist (T) and Counter-Terrorist (CT) sides.`,
    };
  }
   if (i === 1) {
    return {
      id: `viz-2`,
      title: `Distribution of Round End Reasons`,
      imageUrl: `https://i.postimg.cc/T3Pr3D2R/02-round-end-reasons.png`,
      description: `A pie chart illustrating the most common reasons a round ends, such as bomb defusal, bomb explosion, or team elimination.`,
    };
  }
  if (i === 2) {
    return {
      id: `viz-3`,
      title: `T-Side Win Rate by Headshot Rate`,
      imageUrl: `https://i.postimg.cc/bwvQwtYq/03-headshot-rate-vs-wins.png`,
      description: `A scatter plot showing the correlation between T-side headshot percentage and win rate, with a regression line indicating the positive trend.`,
    };
  }
   if (i === 3) {
    return {
      id: `viz-4`,
      title: `Weapon Usage by Winner`,
      imageUrl: `https://i.postimg.cc/fRbxR9W4/04-weapon-usage-by-winner.png`,
      description: `A stacked bar chart comparing the most frequently used weapons by winning and losing teams.`,
    };
  }
  if (i === 4) {
    return {
      id: `viz-5`,
      title: `Kill Distance Distribution`,
      imageUrl: `https://i.postimg.cc/RZ0cZHSj/05-kill-distance-distribution.png`,
      description: `A histogram showing the frequency of kills at various distances, revealing engagement patterns.`,
    };
  }
  if (i === 5) {
    return {
      id: `viz-6`,
      title: `Correlation Heatmap`,
      imageUrl: `https://i.postimg.cc/yYjmKPKs/06-correlation-heatmap.png`,
      description: `A heatmap visualizing the correlation between different match statistics, highlighting relationships between variables.`,
    };
  }
  if (i === 6) {
    return {
      id: `viz-7`,
      title: `Average Kills by Match Outcome`,
      imageUrl: `https://i.postimg.cc/7Y934Vkd/07-kills-by-outcome.png`,
      description: `A box plot comparing the distribution of average kills for winning and losing teams.`,
    };
  }
  if (i === 7) {
    return {
      id: `viz-8`,
      title: `Q-Q Plots for Normality`,
      imageUrl: `https://i.postimg.cc/dt62FBFv/08-qq-plots-normality.png`,
      description: `Q-Q plots assessing the normality of key statistical distributions, such as kill/death ratios.`,
    };
  }
  if (i === 8) {
    return {
      id: `viz-9`,
      title: `PCA Explained Variance`,
      imageUrl: `https://i.postimg.cc/65crK0Xh/09-pca-variance.png`,
      description: `A line chart showing the cumulative explained variance by principal components in a PCA analysis.`,
    };
  }
  if (i === 9) {
    return {
      id: `viz-10`,
      title: `PCA Biplot of Team Statistics`,
      imageUrl: `https://i.postimg.cc/15BGSHQp/10-pca-biplot.png`,
      description: `A PCA biplot visualizing the relationships between various team statistics and their impact on principal components.`,
    };
  }
   if (i === 10) {
    return {
      id: `viz-11`,
      title: `Model Performance ROC Curve`,
      imageUrl: `https://i.ibb.co/2kCysxJ/11-model-performance.png`,
      description: `A Receiver Operating Characteristic (ROC) curve evaluating the performance of the classification model, showing its diagnostic ability.`,
    };
  }
  if (i === 11) {
    return {
      id: `viz-12`,
      title: `Feature Importance Analysis`,
      imageUrl: `https://i.postimg.cc/sDmYzcrY/12-feature-importance.png`,
      description: `An analysis of feature importance, highlighting the key factors that contribute to match outcomes.`,
    };
  }
  if (i === 12) {
    return {
      id: `viz-13`,
      title: `Win Rate by Match Duration`,
      imageUrl: `https://i.postimg.cc/kXqQLHkS/13-win-rate-by-match.png`,
      description: `Analysis of how win rates are influenced by the total duration of a match, highlighting performance over time.`,
    };
  }
  return {
    id: `viz-${i + 1}`,
    title: `Visualization ${i + 1}`,
    imageUrl: `https://picsum.photos/seed/${i + 1}/800/600`,
    description: `Placeholder for visualization ${i + 1}. This will be replaced with a real chart and description.`,
  };
});


export function DataExplorationTab() {
  const cardClassName = "shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border-white/10 rounded-xl min-h-[300px]";
  const [selectedViz, setSelectedViz] = useState(visualizations[0]);

  const handleValueChange = (value: string) => {
    const viz = visualizations.find(v => v.id === value);
    if (viz) {
      setSelectedViz(viz);
    }
  }

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
              <CardContent className="space-y-6">
                <Select onValueChange={handleValueChange} defaultValue={selectedViz.id}>
                  <SelectTrigger className="w-full max-w-md mx-auto bg-black/20 border-white/20">
                    <SelectValue placeholder="Select a visualization" />
                  </SelectTrigger>
                  <SelectContent>
                    {visualizations.map((viz) => (
                      <SelectItem key={viz.id} value={viz.id}>
                        {viz.title}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                {selectedViz && (
                  <div className="p-1">
                     <Card className="bg-black/20 border-white/10 max-w-3xl mx-auto">
                      <CardContent className="flex flex-col items-center justify-center p-6 gap-4">
                         <div className="relative w-full aspect-video rounded-lg overflow-hidden">
                          <Image
                            src={selectedViz.imageUrl}
                            alt={selectedViz.title}
                            fill
                            className="object-contain"
                            data-ai-hint="chart data"
                          />
                         </div>
                        <div className="text-center">
                          <h3 className="text-lg font-semibold text-white">{selectedViz.title}</h3>
                          <p className="text-sm text-white/70">{selectedViz.description}</p>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
}
