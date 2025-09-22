import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function IntroductionTab() {
  return (
    <Card className="shadow-sm">
      <CardHeader>
        <CardTitle className="text-3xl font-bold text-primary">Counter-Strike Match Prediction</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-lg text-foreground/80 max-w-4xl">
          This project focuses on predicting the outcomes of Counter-Strike matches using data analysis and machine learning techniques. The goal is to understand patterns, improve prediction accuracy, and provide insights into competitive gaming.
        </p>
      </CardContent>
    </Card>
  );
}
