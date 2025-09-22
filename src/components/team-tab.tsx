import { PlaceHolderImages } from '@/lib/placeholder-images';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

const teamMembers = [
  { name: 'Chetan Mohnot', role: 'Data Scientist', imageId: 'chetan-mohnot', fallback: 'CM' },
  { name: 'Alex Johnson', role: 'Research Analyst', imageId: 'teammate-2', fallback: 'AJ' },
  { name: 'Samantha Lee', role: 'Developer', imageId: 'teammate-3', fallback: 'SL' },
];

export function TeamTab() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {teamMembers.map((member) => {
        const placeholder = PlaceHolderImages.find(p => p.id === member.imageId);
        return (
          <Card key={member.name} className="text-center shadow-lg hover:shadow-xl transition-shadow duration-300 rounded-lg">
            <CardHeader className="items-center pt-8">
              {placeholder && (
                 <Avatar className="w-24 h-24 border-4 border-primary/20">
                    <AvatarImage
                        src={placeholder.imageUrl}
                        alt={`Portrait of ${member.name}`}
                        data-ai-hint={placeholder.imageHint}
                    />
                    <AvatarFallback>{member.fallback}</AvatarFallback>
                </Avatar>
              )}
            </CardHeader>
            <CardContent className="pb-8">
              <CardTitle className="text-xl font-semibold">{member.name}</CardTitle>
              <p className="text-muted-foreground">{member.role}</p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
