
'use client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { CheckCircle2 } from 'lucide-react';

const models = [
  {
    title: 'Frequent Pattern Mining',
    description: 'Uncovering hidden patterns and associations in player behavior and team strategies (e.g., Apriori, FP-Growth).',
    details: {
      choice: 'Why the model was chosen (justify selection based on dataset characteristics).',
      assumptions: 'Model assumptions (e.g., specifics of FP-Growth or Apriori).',
      tuning: 'Hyperparameter tuning (adjustments to improve model performance).',
      challenges: 'Challenges faced & solutions (if applicable).',
    },
    evaluation: ['Support', 'Confidence', 'Lift']
  },
  {
    title: 'Classification',
    description: 'Predicting discrete outcomes like match winner or round winner (e.g., Decision Trees, SVM, k-NN).',
    details: {
      choice: 'Why the model was chosen (justify selection based on dataset characteristics).',
      assumptions: 'Model assumptions (e.g., SVM assumes data is linearly separable).',
      tuning: 'Hyperparameter tuning (adjustments to improve model performance).',
      challenges: 'Challenges faced & solutions (if applicable).',
    },
    evaluation: ['Accuracy', 'Precision', 'Recall', 'F1-score', 'ROC-AUC']
  },
  {
    title: 'Clustering',
    description: 'Grouping players or teams based on similarities in their playstyle or performance metrics (e.g., K-Means, DBSCAN).',
    details: {
      choice: 'Why the model was chosen (justify selection based on dataset characteristics).',
      assumptions: 'Model assumptions (e.g., K-Means assumes spherical clusters).',
      tuning: 'Hyperparameter tuning (adjustments to improve model performance).',
      challenges: 'Challenges faced & solutions (if applicable).',
    },
    evaluation: ['Silhouette Score', 'Davies-Bouldin Index']
  },
  {
    title: 'Regression',
    description: 'Forecasting continuous values such as player K/D ratio or match duration (e.g., Linear, Logistic).',
    details: {
      choice: 'Why the model was chosen (justify selection based on dataset characteristics).',
      assumptions: 'Model assumptions (e.g., Linear Regression assumes a linear relationship).',
      tuning: 'Hyperparameter tuning (adjustments to improve model performance).',
      challenges: 'Challenges faced & solutions (if applicable).',
    },
    evaluation: ['RMSE', 'MSE', 'R²-score']
  }
];

export function ModelsImplementedTab() {
  const cardClassName = "shadow-lg transition-shadow bg-black/30 backdrop-blur-sm border-white/10 rounded-xl";

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
          Models <span className="text-primary">Implemented</span>
        </h1>
        <p className="mt-4 text-lg leading-8 text-white/80 max-w-4xl mx-auto">
          This section showcases the machine learning models implemented, their performance, and the data transformations required.
        </p>
      </div>

      <Card className={cardClassName}>
        <CardHeader>
          <CardTitle className="text-2xl text-primary">Model Categories</CardTitle>
          <CardDescription className="text-white/80">
            Each team must implement at least four machine-learning models from different categories. Click on a model type to see more details.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid md:grid-cols-2 gap-6">
          {models.map((model) => (
            <Dialog key={model.title}>
              <DialogTrigger asChild>
                <Card className="bg-black/20 border-white/10 hover:bg-black/40 hover:border-primary/50 cursor-pointer transition-all flex flex-col">
                  <CardHeader>
                    <CardTitle className="text-xl text-white">{model.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="flex-grow">
                    <p className="text-white/70">{model.description}</p>
                  </CardContent>
                </Card>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md bg-black/50 backdrop-blur-md border-white/20 text-white">
                <DialogHeader>
                  <DialogTitle className="text-2xl text-primary">{model.title}</DialogTitle>
                </DialogHeader>
                <div className="py-4 space-y-4 text-white/80">
                    <div>
                        <h4 className='font-semibold text-lg text-white'>Justification</h4>
                        <p>{model.details.choice}</p>
                    </div>
                     <div>
                        <h4 className='font-semibold text-lg text-white'>Assumptions</h4>
                        <p>{model.details.assumptions}</p>
                    </div>
                     <div>
                        <h4 className='font-semibold text-lg text-white'>Hyperparameter Tuning</h4>
                        <p>{model.details.tuning}</p>
                    </div>
                     <div>
                        <h4 className='font-semibold text-lg text-white'>Challenges</h4>
                        <p>{model.details.challenges}</p>
                    </div>
                     <div>
                        <h4 className='font-semibold text-lg text-white'>Evaluation Metrics</h4>
                        <ul className='list-disc list-inside'>
                            {model.evaluation.map(metric => <li key={metric}>{metric}</li>)}
                        </ul>
                    </div>
                </div>
              </DialogContent>
            </Dialog>
          ))}
        </CardContent>
      </Card>
      
      <div className="grid md:grid-cols-2 gap-8">
        <Card className={cardClassName}>
            <CardHeader>
                <CardTitle className="text-2xl text-primary">Performance Evaluation</CardTitle>
                <CardDescription className="text-white/80">Comparing model performances to identify the most effective approaches for our dataset.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-white/80">
                <p>Each team must select appropriate evaluation metrics based on the model type and compare model performances to explain which approach worked best.</p>
                <ul className="space-y-2">
                    <li className='flex items-start gap-2'><CheckCircle2 className="h-5 w-5 text-green-400 mt-1 flex-shrink-0" /><span>Justify why one model performs better than another for the specific dataset.</span></li>
                    <li className='flex items-start gap-2'><CheckCircle2 className="h-5 w-5 text-green-400 mt-1 flex-shrink-0" /><span>Provide a clear comparison of the results.</span></li>
                </ul>
            </CardContent>
        </Card>
         <Card className={cardClassName}>
            <CardHeader>
                <CardTitle className="text-2xl text-primary">Data Formatting for Models</CardTitle>
                <CardDescription className="text-white/80">Ensuring that dataset transformations align with model requirements.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 text-white/80">
                <p>Data must be formatted correctly for each model. For example, SVMs require numerical data, while Decision Trees can handle categorical variables. Clustering algorithms may require feature scaling.</p>
                <ul className="space-y-2">
                    <li className='flex items-start gap-2'><CheckCircle2 className="h-5 w-5 text-green-400 mt-1 flex-shrink-0" /><span>Categorical features must be converted for certain models.</span></li>
                    <li className='flex items-start gap-2'><CheckCircle2 className="h-5 w-5 text-green-400 mt-1 flex-shrink-0" /><span>Include before-and-after data transformation snapshots to show preprocessing steps.</span></li>
                </ul>
            </CardContent>
        </Card>
      </div>
    </div>
  );
}
