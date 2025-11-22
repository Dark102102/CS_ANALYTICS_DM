
'use client';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { CheckCircle2 } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"


const models = [
  {
    title: 'Frequent Pattern Mining',
    description: 'Uncovering hidden patterns and associations in player behavior and team strategies (e.g., Apriori, FP-Growth).',
    details: {
      content: (
          <div className="space-y-6">
            <div>
              <h4 className='font-semibold text-lg text-white mb-2'>Justification</h4>
              <p>The Frequent Pattern Mining analysis revealed several meaningful and interpretable relationships driving round outcomes in professional CS2 matches. Using Apriori and FP-Growth, we identified strong co-occurring tactical patterns across rounds and quantified their importance using support, confidence, and lift.</p>
            </div>
             <div>
              <h4 className='font-semibold text-lg text-white mb-2'>Key Insights</h4>
               <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Rule</TableHead>
                    <TableHead>Confidence</TableHead>
                    <TableHead>Lift</TableHead>
                    <TableHead>Interpretation</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>BOMB_PLANTED + HIGH_HS_RATE → T_WIN</TableCell>
                    <TableCell>0.943</TableCell>
                    <TableCell>2.088</TableCell>
                    <TableCell>Strong aim + plant leads to wins</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>CT_LEADING + HIGH_HS_RATE → T_WIN</TableCell>
                    <TableCell>0.926</TableCell>
                    <TableCell>2.050</TableCell>
                    <TableCell>Ts overcome score deficits via accuracy</TableCell>
                  </TableRow>
                   <TableRow>
                    <TableCell>MID_ROUND + BOMB_PLANTED → T_WIN</TableCell>
                    <TableCell>0.790</TableCell>
                    <TableCell>1.750</TableCell>
                    <TableCell>Mid-round executes highly successful</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>BOMB_DEFUSED → CT_WIN</TableCell>
                    <TableCell>1.000</TableCell>
                    <TableCell>1.953</TableCell>
                    <TableCell>Objective-centric CT victories</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </div>
            <div>
              <h4 className='font-semibold text-lg text-white mb-2'>Assumptions</h4>
              <p>The model assumes that transaction data is available and that the support threshold is appropriately set to capture relevant patterns without generating excessive noise. We found that CT-side wins are heavily tied to objective control rather than mechanical dominance.</p>
            </div>
            <div>
              <h4 className='font-semibold text-lg text-white mb-2'>Hyperparameter Tuning</h4>
              <p>Hyperparameter tuning involved adjusting the minimum support and confidence thresholds to balance between finding frequent and meaningful patterns.</p>
            </div>
            <div>
              <h4 className='font-semibold text-lg text-white mb-2'>Challenges</h4>
              <p>A key challenge was interpreting the vast number of generated rules. We focused on rules with high confidence and lift to identify the most impactful tactical patterns, such as the link between headshot rates and T-side wins.</p>
            </div>
            <div>
                <h4 className='font-semibold text-lg text-white'>Conclusion</h4>
                <p>The results show that T-side victories are consistently associated with rounds where players achieve high headshot accuracy, especially when combined with successful bomb plants. Patterns involving “BOMB_DEFUSED → CT_WIN” highlight that CTs succeed most consistently when they maintain site presence long enough to defuse or completely deny plants.</p>
            </div>
          </div>
      ),
    },
    evaluation: ['Support', 'Confidence', 'Lift']
  },
  {
    title: 'Classification',
    description: 'Predicting discrete outcomes like match winner or round winner (e.g., Decision Trees, SVM, k-NN).',
    details: {
      content: (
        <div className="space-y-6">
          <div>
            <h4 className='font-semibold text-lg text-white mb-2'>Models Implemented</h4>
            <div className="space-y-4">
              <div className="border-l-4 border-primary/30 pl-4">
                <h5 className="font-semibold text-white">Decision Tree Classifier</h5>
                <p><span className="font-medium text-white/90">Justification:</span> Selected because it performs well on datasets with numerical features and can naturally model nonlinear relationships.</p>
                <p><span className="font-medium text-white/90">Assumptions:</span> Assumes data can be recursively partitioned into pure subsets; does not assume linearity.</p>
                <p><span className="font-medium text-white/90">Tuning:</span> Best parameters from GridSearchCV were `max_depth=None`, `min_samples_leaf=1`, `min_samples_split=2`.</p>
              </div>
              <div className="border-l-4 border-primary/30 pl-4">
                <h5 className="font-semibold text-white">Support Vector Machine (Linear)</h5>
                <p><span className="font-medium text-white/90">Justification:</span> Ideal for fully numeric, scaled datasets to separate CT-win vs. CT-loss classes.</p>
                <p><span className="font-medium text-white/90">Assumptions:</span> Assumes classes are approximately linearly separable and features are correctly scaled.</p>
                <p><span className="font-medium text-white/90">Tuning:</span> Best parameters were `C=0.1`, `gamma='scale'`, `kernel='linear'`.</p>
              </div>
              <div className="border-l-4 border-primary/30 pl-4">
                <h5 className="font-semibold text-white">Random Forest Classifier</h5>
                <p><span className="font-medium text-white/90">Justification:</span> Robust ensemble model that reduces overfitting and captures nonlinear relationships well on smaller datasets.</p>
                <p><span className="font-medium text-white/90">Assumptions:</span> Assumes combining many decorrelated trees reduces variance and improves generalization.</p>
                <p><span className="font-medium text-white/90">Tuning:</span> Best parameters were `n_estimators=100`, `max_depth=None`, `min_samples_split=2`.</p>
              </div>
              <div className="border-l-4 border-primary/30 pl-4">
                <h5 className="font-semibold text-white">k-Nearest Neighbors (KNN)</h5>
                <p><span className="font-medium text-white/90">Justification:</span> Provides a simple baseline for comparison, suitable for scaled numeric datasets.</p>
                <p><span className="font-medium text-white/90">Assumptions:</span> Assumes similar data points are close in feature space and features are equally scaled.</p>
                <p><span className="font-medium text-white/90">Tuning:</span> Best parameters were `n_neighbors=7`, `p=1` (Manhattan), `weights='distance'`.</p>
              </div>
            </div>
          </div>
          <div>
            <h4 className='font-semibold text-lg text-white mb-2'>Performance Comparison</h4>
             <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Model</TableHead>
                  <TableHead>Accuracy</TableHead>
                  <TableHead>Precision</TableHead>
                  <TableHead>Recall</TableHead>
                  <TableHead>F1-score</TableHead>
                  <TableHead>ROC-AUC</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableRow>
                  <TableCell>Decision Tree</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>SVM (Linear)</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Random Forest</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                  <TableCell>1.00</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>KNN</TableCell>
                  <TableCell>0.896</TableCell>
                  <TableCell>0.862</TableCell>
                  <TableCell>0.962</TableCell>
                  <TableCell>0.909</TableCell>
                  <TableCell>0.979</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </div>
          <div>
            <h4 className='font-semibold text-lg text-white mb-2'>Conclusion</h4>
            <p>Although Decision Tree, SVM, and Random Forest all achieved perfect scores, **Random Forest is the most reliable best model**. It is more robust to noise than a single Decision Tree, carries less risk of overfitting, and offers strong generalization via its tree ensemble. KNN performed well but was weaker due to its sensitivity to noisy boundaries. All models demonstrated high performance, with Random Forest being the best overall due to its stability and robustness.</p>
          </div>
        </div>
      ),
    },
    evaluation: ['Accuracy', 'Precision', 'Recall', 'F1-score', 'ROC-AUC']
  },
  {
    title: 'Clustering',
    description: 'Grouping players or teams based on similarities in their playstyle or performance metrics (e.g., K-Means, DBSCAN).',
    details: {
      choice: 'The clustering analysis successfully segmented players into two clearly distinguishable performance-based roles: Entry Fraggers and Balanced Players. By applying K-Means on normalized player statistics, we observed distinct behavioral archetypes grounded in in-game performance patterns. Entry Fraggers formed a smaller but more aggressive cluster characterized by high opening duel attempts, elevated kill counts, strong KD ratios, and frequent multi-kill rounds. Their statistical profile reflects high-risk, high-reward gameplay that emphasizes creating early space and initiating engagements.',
      assumptions: 'K-Means assumes that clusters are spherical and of similar size. The relatively strong silhouette score confirmed that the feature space was well-suited for this method, capturing meaningful differences in player tendencies. The Balanced Player cluster consisted of a larger group of individuals exhibiting consistent and supportive gameplay. These players showed higher headshot percentages, more assists, and steadier round-to-round performance metrics, indicating a playstyle focused on maintaining structure, trading kills, and anchoring positions rather than driving aggressive entries.',
      tuning: 'The number of clusters (k) was tuned, with k=2 providing the most interpretable and distinct player archetypes (Entry Fraggers vs. Balanced Players).',
      challenges: 'The main challenge was ensuring the clusters were not just statistically significant but also interpretable in the context of CS2 gameplay. This was validated by analyzing the feature distributions for each cluster. The clustering results therefore provide actionable insights into role identity and team composition in competitive CS2 play.',
    },
    evaluation: ['Silhouette Score', 'Davies-Bouldin Index']
  },
  {
    title: 'Regression',
    description: 'Forecasting continuous values such as player K/D ratio or match duration (e.g., Linear, Logistic).',
    details: {
      choice: 'The regression models produced strong predictive performance, showing that player damage output is highly explainable using core combat statistics such as kills, deaths, headshot rate, and average kill distance. Among the three regression models—Linear Regression, Ridge Regression, and Bayesian Ridge Regression—performance remained consistently high across all metrics. Each model achieved an R² near or above 0.90, demonstrating that a large portion of the variance in total damage can be captured by straightforward linear relationships.',
      assumptions: 'Linear regression models assume a linear relationship between features and the target variable. The high R² values confirmed that damage output in CS2 is driven by predictable, linear mechanics. The baseline Linear Regression model emerged as the strongest performer overall, with the lowest RMSE and highest R².',
      tuning: 'Minimal hyperparameter tuning was needed as the baseline Linear Regression model performed strongest. Ridge and Bayesian Ridge models showed that regularization offered limited improvement, indicating low multicollinearity.',
      challenges: 'The primary challenge was selecting the right features. The analysis confirmed that standard combat metrics were sufficient, reinforcing that CS2 performance data contains clear, measurable patterns suitable for linear modeling.',
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
              <DialogContent className="sm:max-w-2xl bg-black/50 backdrop-blur-md border-white/20 text-white">
                <DialogHeader>
                  <DialogTitle className="text-2xl text-primary">{model.title}</DialogTitle>
                </DialogHeader>
                <div className="py-4 space-y-4 text-white/80 max-h-[80vh] overflow-y-auto pr-4">
                  {model.details.content ? (
                    model.details.content
                  ) : (
                    <div className="space-y-6">
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
                    </div>
                  )}
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
