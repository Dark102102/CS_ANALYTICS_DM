'use server';

import { generateEsportsInsights, GenerateEsportsInsightsInput } from '@/ai/flows/generate-esports-insights';
import { z } from 'zod';

const schema = z.object({
  matchData: z.string().min(10, { message: 'Match data must be at least 10 characters long.' }),
});

type FormState = {
  message: string;
  errors: { matchData?: string[] } | null;
  data: { insights: string } | null;
}

export async function handleGenerateInsights(prevState: FormState, formData: FormData): Promise<FormState> {
  const validatedFields = schema.safeParse({
    matchData: formData.get('matchData'),
  });

  if (!validatedFields.success) {
    return {
      message: 'Invalid form data.',
      errors: validatedFields.error.flatten().fieldErrors,
      data: null,
    };
  }

  try {
    const input: GenerateEsportsInsightsInput = {
      matchData: validatedFields.data.matchData,
    };
    const result = await generateEsportsInsights(input);
    return {
      message: 'Insights generated successfully.',
      errors: null,
      data: result,
    };
  } catch (error) {
    console.error('Error generating insights:', error);
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred.';
    return {
      message: `Failed to generate insights: ${errorMessage}`,
      errors: null,
      data: null,
    };
  }
}
