'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { handleGenerateInsights } from '@/app/actions';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { useEffect, useRef } from 'react';
import { useToast } from '@/hooks/use-toast';
import { Bot, Loader2 } from 'lucide-react';

const initialState = {
  message: '',
  errors: null,
  data: null,
};

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending} className="w-full md:w-auto">
      {pending ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Generating...
        </>
      ) : (
        <>
          <Bot className="mr-2 h-4 w-4" />
          Generate Insights
        </>
      )}
    </Button>
  );
}

export function EsportsInsightGenerator() {
  const [state, formAction] = useFormState(handleGenerateInsights, initialState);
  const { toast } = useToast();
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    if (state.message && (state.errors || state.message.startsWith('Failed'))) {
      toast({
        title: 'Error',
        description: state.message,
        variant: 'destructive',
      });
    }
    if(state.message && !state.errors && state.data) {
        formRef.current?.reset();
    }
  }, [state, toast]);

  return (
    <div className="grid gap-8 md:grid-cols-2">
      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>Esports Insight Generator</CardTitle>
          <CardDescription>
            Enter match data, player stats, and team performance info to generate key insights. For example, explore which stats have the biggest impact on outcomes.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form ref={formRef} action={formAction} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="matchData">Match Data</Label>
              <Textarea
                id="matchData"
                name="matchData"
                placeholder="Paste your match data here... (e.g., player K/D/A, map scores, team economy)"
                className="min-h-[200px]"
                required
              />
               {state.errors?.matchData && (
                <p className="text-sm font-medium text-destructive">
                  {state.errors.matchData[0]}
                </p>
              )}
            </div>
            <SubmitButton />
          </form>
        </CardContent>
      </Card>
      <Card className="flex flex-col shadow-sm">
        <CardHeader>
          <CardTitle>Generated Insights</CardTitle>
          <CardDescription>The AI-powered analysis will appear below.</CardDescription>
        </CardHeader>
        <CardContent className="flex-grow">
          {useFormStatus().pending ? (
            <div className="flex items-center justify-center h-full text-muted-foreground">
               <Loader2 className="mr-2 h-8 w-8 animate-spin text-primary" />
            </div>
          ) : state.data ? (
            <div className="space-y-4 text-sm text-foreground/90 whitespace-pre-wrap p-4 bg-muted/50 rounded-md h-full">
              <p>{state.data.insights}</p>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-muted-foreground rounded-md border-2 border-dashed">
              <p>No insights generated yet.</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
