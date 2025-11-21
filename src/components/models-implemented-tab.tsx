
'use client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';

const models = [
  {
    title: 'Frequent Pattern Mining',
    description: 'Uncovering hidden patterns and associations in player behavior and team strategies.',
    details: 'This section will elaborate on the frequent pattern mining techniques used, such as Apriori or FP-Growth, to discover interesting relationships in the game data. Placeholder for more detailed content.'
  },
  {
    title: 'Classification',
    description: 'Predicting discrete outcomes like match winner or round winner.',
    details: 'This section will detail the classification models (e.g., Logistic Regression, SVM, Random Forest) built to predict match outcomes. Placeholder for model performance, feature importance, and other specifics.'
  },
  {
    title: 'Clustering',
    description: 'Grouping players or teams based on similarities in their playstyle or performance metrics.',
    details: 'Here we will discuss the clustering algorithms (e.g., K-Means, DBSCAN) used to identify distinct player archetypes or team strategies from the data. Placeholder for detailed cluster analysis.'
  },
  {
    title: 'Regression',
    description: 'Forecasting continuous values such as player K/D ratio or match duration.',
    details: 'This part will cover the regression models developed to predict numerical outcomes. Details on model architecture, evaluation metrics, and results will be presented here. Placeholder for more content.'
  }
];

export function ModelsImplementedTab() {
  const cardClassName = "shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border-white/10 rounded-xl min-h-[300px]";

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
          Models <span className="text-primary">Implemented</span>
        </h1>
        <p className="mt-4 text-lg leading-8 text-white/80 max-w-3xl mx-auto">
          Explore the various machine learning models we've implemented to analyze and predict game outcomes.
        </p>
      </div>

      <Card className={cardClassName}>
        <CardHeader>
          <CardTitle className="text-2xl text-primary">Model Categories</CardTitle>
          <CardDescription className="text-white/80">
            Click on a model type to see more details about the implementation.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid md:grid-cols-2 gap-6">
          {models.map((model) => (
            <Dialog key={model.title}>
              <DialogTrigger asChild>
                <Card className="bg-black/20 border-white/10 hover:bg-black/40 hover:border-primary/50 cursor-pointer transition-all">
                  <CardHeader>
                    <CardTitle className="text-xl text-white">{model.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-white/70">{model.description}</p>
                  </CardContent>
                </Card>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px] bg-black/50 backdrop-blur-md border-white/20 text-white">
                <DialogHeader>
                  <DialogTitle className="text-2xl text-primary">{model.title}</DialogTitle>
                </DialogHeader>
                <div className="py-4 text-white/80">
                  {model.details}
                </div>
              </DialogContent>
            </Dialog>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
