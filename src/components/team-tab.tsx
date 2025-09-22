
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
import { Mail, Linkedin } from 'lucide-react';

const teamMembers = [
  {
    name: 'Chetan Mohnot',
    role: 'Data Scientist',
    imageId: 'chetan-mohnot',
    fallback: 'CM',
    bio: 'Chetan is a data scientist specializing in machine learning and statistical analysis for sports analytics. He is passionate about uncovering insights from data to predict match outcomes and enhance team strategies.',
    fullImageId: 'chetan-mohnot-full',
    email: 'chetan.mohnot@example.com',
    linkedin: '#',
    avatarUrl: 'https://storage.googleapis.com/aifirebase-799a7.appspot.com/user_images/Chetan%20Mohnot_1723558831969.jpeg',
    fullImageUrl: 'https://storage.googleapis.com/aifirebase-799a7.appspot.com/user_images/Chetan%20Mohnot_1723558831969.jpeg'
  },
  {
    name: 'Alex Johnson',
    role: 'Research Analyst',
    imageId: 'teammate-2',
    fallback: 'AJ',
    bio: 'Alex is an expert in data collection and research methodologies for competitive gaming analysis. She has a keen eye for detail and a deep understanding of the esports landscape.',
    fullImageId: 'teammate-2-full',
    email: 'alex.johnson@example.com',
    linkedin: '#',
  },
  {
    name: 'Adwait Bapat',
    role: 'Developer',
    imageId: 'adwait-bapat',
    fallback: 'AB',
    bio: 'Adwait is a full-stack developer focused on building scalable data processing and visualization tools. His expertise in software engineering brings our analytical models to life.',
    fullImageId: 'adwait-bapat-full',
    email: 'adwait.bapat@example.com',
    linkedin: '#',
    avatarUrl: 'https://storage.googleapis.com/aifirebase-799a7.appspot.com/user_images/i_dont_know_what_i_am_doing_1723558110901.jpeg',
    fullImageUrl: 'https://storage.googleapis.com/aifirebase-799a7.appspot.com/user_images/i_dont_know_what_i_am_doing_1723558110901.jpeg'
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
          const isHardcoded = member.name === 'Adwait Bapat' || member.name === 'Chetan Mohnot';
          const placeholder = !isHardcoded ? PlaceHolderImages.find(p => p.id === member.imageId) : null;
          const fullPlaceholder = !isHardcoded ? PlaceHolderImages.find(p => p.id === member.fullImageId) : null;

          const avatarUrl = isHardcoded ? member.avatarUrl : placeholder?.imageUrl;
          const fullImageUrl = isHardcoded ? member.fullImageUrl : fullPlaceholder?.imageUrl;
          const imageHint = placeholder?.imageHint || 'person portrait';


          return (
            <Dialog key={member.name}>
                <Card className="text-center shadow-lg hover:shadow-xl transition-shadow duration-300 rounded-lg flex flex-col">
                  <DialogTrigger asChild>
                    <div className='cursor-pointer flex-grow'>
                      <CardHeader className="items-center pt-8">
                        {avatarUrl && (
                          <Avatar className="w-24 h-24 border-4 border-primary/20">
                            <AvatarImage
                              src={avatarUrl}
                              alt={`Portrait of ${member.name}`}
                              data-ai-hint={imageHint}
                            />
                            <AvatarFallback>{member.fallback}</AvatarFallback>
                          </Avatar>
                        )}
                      </CardHeader>
                      <CardContent>
                        <CardTitle className="text-xl font-semibold">{member.name}</CardTitle>
                        <p className="text-primary">{member.role}</p>
                      </CardContent>
                    </div>
                  </DialogTrigger>
                  <CardContent className="pb-8 pt-2">
                     <div className="mt-2 flex items-center justify-center space-x-4">
                        <a href={`mailto:${member.email}`} className="text-muted-foreground hover:text-primary transition-colors">
                          <Mail className="h-6 w-6" />
                          <span className="sr-only">Email</span>
                        </a>
                        <a href={member.linkedin} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-primary transition-colors">
                          <Linkedin className="h-6 w-6" />
                          <span className="sr-only">LinkedIn</span>
                        </a>
                      </div>
                  </CardContent>
                </Card>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle className="text-2xl">{member.name}</DialogTitle>
                </DialogHeader>
                <div className="py-4">
                  {fullImageUrl && (
                     <div className="mb-4 rounded-lg overflow-hidden">
                        <Image
                            src={fullImageUrl}
                            alt={`Portrait of ${member.name}`}
                            width={400}
                            height={400}
                            className="w-full h-auto object-cover"
                            data-ai-hint={imageHint}
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
