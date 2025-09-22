
'use client';

import { PlaceHolderImages } from '@/lib/placeholder-images';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import Image from 'next/image';

const teamMembers = [
  {
    name: 'Chetan Mohnot',
    role: 'Data Scientist',
    imageId: 'chetan-mohnot',
    fallback: 'CM',
    bio: 'Chetan is a data scientist specializing in machine learning and statistical analysis for sports analytics. He is passionate about uncovering insights from data to predict match outcomes and enhance team strategies.',
    fullImageId: 'chetan-mohnot-full',
  },
  {
    name: 'Alex Johnson',
    role: 'Research Analyst',
    imageId: 'teammate-2',
    fallback: 'AJ',
    bio: 'Alex is an expert in data collection and research methodologies for competitive gaming analysis. She has a keen eye for detail and a deep understanding of the esports landscape.',
    fullImageId: 'teammate-2-full',
  },
  {
    name: 'Samantha Lee',
    role: 'Developer',
    imageId: 'teammate-3',
    fallback: 'SL',
    bio: 'Samantha is a full-stack developer focused on building scalable data processing and visualization tools. Her expertise in software engineering brings our analytical models to life.',
    fullImageId: 'teammate-3-full',
  },
];

export function TeamTab() {
  return (
    <div className="space-y-8">
       <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight">Our Team</h2>
        <p className="mt-2 text-lg text-muted-foreground max-w-2xl mx-auto">
          Meet the dedicated team behind the Counter-Strike match prediction project, bringing together expertise in data science, research, and development.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {teamMembers.map(member => {
          const placeholder = PlaceHolderImages.find(p => p.id === member.imageId);
          const fullPlaceholder = PlaceHolderImages.find(p => p.id === member.fullImageId);

          return (
            <Dialog key={member.name}>
              <DialogTrigger asChild>
                <Card className="text-center shadow-lg hover:shadow-xl transition-shadow duration-300 rounded-lg cursor-pointer">
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
                    <p className="text-primary">{member.role}</p>
                  </CardContent>
                </Card>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle className="text-2xl">{member.name}</DialogTitle>
                </DialogHeader>
                <div className="py-4">
                  {fullPlaceholder && (
                     <div className="mb-4 rounded-lg overflow-hidden">
                        <Image
                            src={fullPlaceholder.imageUrl}
                            alt={`Portrait of ${member.name}`}
                            width={400}
                            height={400}
                            className="w-full h-auto object-cover"
                            data-ai-hint={fullPlaceholder.imageHint}
                        />
                     </div>
                  )}
                  <h3 className="text-lg font-semibold text-primary">{member.role}</h3>
                  <p className="mt-2 text-muted-foreground">{member.bio}</p>
                </div>
              </DialogContent>
            </Dialog>
          );
        })}
      </div>
    </div>
  );
}
