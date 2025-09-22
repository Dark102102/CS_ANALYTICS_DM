
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
    email: 'chmo4618@colorado.edu',
    linkedin: 'https://www.linkedin.com/in/chetan-mohnot/',
    avatarUrl: 'https://i.postimg.cc/x88zWT27/Chetan-Mohnot-1.jpg',
    fullImageUrl: 'https://i.postimg.cc/x88zWT27/Chetan-Mohnot-1.jpg'
  },
  {
    name: 'Luke Robinson',
    role: 'Research Analyst',
    imageId: 'luke-robinson',
    fallback: 'LR',
    bio: 'Luke is an expert in data collection and research methodologies for competitive gaming analysis. He has a keen eye for detail and a deep understanding of the esports landscape.',
    fullImageId: 'luke-robinson-full',
    email: 'luke.robinson@example.com',
    linkedin: '#',
    avatarUrl: 'https://i.postimg.cc/NjBHc4Bm/Luke-Robinson.jpg',
    fullImageUrl: 'https://i.postimg.cc/NjBHc4Bm/Luke-Robinson.jpg'
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
    avatarUrl: 'https://i.postimg.cc/W1Bwgrv4/Adwait-Bapat.jpg',
    fullImageUrl: 'https://i.postimg.cc/W1Bwgrv4/Adwait-Bapat.jpg',
  },
];

export function TeamTab() {
  return (
    <div className="space-y-8">
       <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight text-white">Our <span className="text-primary">Team</span></h2>
        <p className="mt-2 text-lg text-white/80 max-w-2xl mx-auto">
          Meet the dedicated team behind the Counter-Strike match prediction project, bringing together expertise in data science, research, and development.
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {teamMembers.map(member => {
          const imageHint = 'person portrait';

          return (
            <Dialog key={member.name}>
                <Card className="text-center shadow-lg hover:shadow-xl transition-shadow duration-300 rounded-xl flex flex-col bg-black/30 backdrop-blur-sm border border-white/10">
                  <DialogTrigger asChild>
                    <div className='cursor-pointer flex-grow'>
                      <CardHeader className="items-center pt-8">
                        <Avatar className="w-24 h-24 border-4 border-primary/20">
                          <AvatarImage
                            src={member.avatarUrl}
                            alt={`Portrait of ${member.name}`}
                            data-ai-hint={imageHint}
                            className="object-cover object-top w-full h-full"
                          />
                          <AvatarFallback>{member.fallback}</AvatarFallback>
                        </Avatar>
                      </CardHeader>
                      <CardContent className="pb-2">
                        <CardTitle className="text-xl font-semibold text-white">{member.name}</CardTitle>
                        <p className="text-primary">{member.role}</p>
                      </CardContent>
                    </div>
                  </DialogTrigger>
                  <CardContent className="pb-8 pt-0">
                     <div className="mt-2 flex items-center justify-center space-x-4">
                        <a href={`mailto:${member.email}`} className="text-white/70 hover:text-primary transition-colors">
                          <Mail className="h-6 w-6" />
                          <span className="sr-only">Email</span>
                        </a>
                        <a href={member.linkedin} target="_blank" rel="noopener noreferrer" className="text-white/70 hover:text-primary transition-colors">
                          <Linkedin className="h-6 w-6" />
                          <span className="sr-only">LinkedIn</span>
                        </a>
                      </div>
                  </CardContent>
                </Card>
              <DialogContent className="sm:max-w-[425px] bg-black/50 backdrop-blur-md border-white/20">
                <DialogHeader>
                  <DialogTitle className="text-2xl text-white">{member.name}</DialogTitle>
                </DialogHeader>
                <div className="py-4">
                   <div className="mb-4 rounded-lg overflow-hidden aspect-square">
                      <Image
                          src={member.fullImageUrl}
                          alt={`Portrait of ${member.name}`}
                          width={400}
                          height={400}
                          className="w-full h-[400px] object-cover object-top"
                          data-ai-hint={imageHint}
                      />
                   </div>
                  <h3 className="text-lg font-semibold text-primary">{member.role}</h3>
                  <p className="mt-2 text-white/80">{member.bio}</p>
                </div>
              </DialogContent>
            </Dialog>
          );
        })}
      </div>
    </div>
  );
}
