import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Newspaper, GraduationCap, Briefcase, Database } from 'lucide-react';
import { ArticlesAdmin } from '@/components/admin/ArticlesAdmin';
import { FormationsAdmin } from '@/components/admin/FormationsAdmin';
import { EmploisAdmin } from '@/components/admin/EmploisAdmin';
import { AggregationManager } from '@/components/admin/AggregationManager';

const Admin = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-deep-navy text-white py-12">
        <div className="max-w-7xl mx-auto px-4 md:px-8">
          <h1 className="font-playfair text-4xl font-bold mb-2">Administration</h1>
          <p className="font-inter text-slate-300">
            Gestion du contenu de la plateforme
          </p>
        </div>
      </div>

      {/* Admin Panel */}
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-12">
        <Tabs defaultValue="articles" className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="articles" data-testid="tab-articles" className="flex items-center space-x-2">
              <Newspaper className="w-4 h-4" />
              <span>Articles</span>
            </TabsTrigger>
            <TabsTrigger value="formations" data-testid="tab-formations" className="flex items-center space-x-2">
              <GraduationCap className="w-4 h-4" />
              <span>Formations</span>
            </TabsTrigger>
            <TabsTrigger value="emplois" data-testid="tab-emplois" className="flex items-center space-x-2">
              <Briefcase className="w-4 h-4" />
              <span>Emplois</span>
            </TabsTrigger>
            <TabsTrigger value="aggregation" data-testid="tab-aggregation" className="flex items-center space-x-2">
              <Database className="w-4 h-4" />
              <span>Agrégation</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="articles">
            <ArticlesAdmin />
          </TabsContent>

          <TabsContent value="formations">
            <FormationsAdmin />
          </TabsContent>

          <TabsContent value="emplois">
            <EmploisAdmin />
          </TabsContent>

          <TabsContent value="aggregation">
            <AggregationManager />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Admin;