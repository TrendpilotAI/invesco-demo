# 215 — Invesco Retention: Skeleton Loaders & AI Animation (P1)

**Priority:** 🟠 P1 — Makes AI feel real, not static  
**Project:** invesco-retention  
**Effort:** S (2-3 hrs)  
**Owner:** Honey  
**Dependencies:** None (can do before deploy)

---

## Task Description

Currently the signal results "just appear" — clicking search shows instant data. This makes the AI feel like a database lookup, not intelligence. Adding a 1.5-2s "AI analyzing signals..." animation with skeleton loaders before results appear transforms the perception of the product.

Brian Kiley is mobile-first. This animation must look polished on phones. The skeleton loaders should mimic the exact shape of the result cards that will appear.

---

## Coding Prompt (Agent-Executable)

```
You are adding skeleton loaders and an AI analysis animation to the invesco-retention demo app.

REPO: /data/workspace/projects/invesco-retention/demo-app

TASK:

1. Find the signal results component. Look in:
   - src/app/signals/page.tsx
   - src/components/signals/SignalResults.tsx (or similar)
   Run: grep -r "signal\|result\|advisor" src/ --include="*.tsx" -l

2. Add a loading state to the signal search/query flow:

   ```typescript
   const [isAnalyzing, setIsAnalyzing] = useState(false);
   
   const handleSearch = async (query: string) => {
     setIsAnalyzing(true);
     // Fake AI processing delay
     await new Promise(resolve => setTimeout(resolve, 1800));
     setIsAnalyzing(false);
     // Show results
     setResults(getFilteredAdvisors(query));
   };
   ```

3. Create a SkeletonCard component that mimics an advisor result card:

   ```tsx
   const SkeletonCard = () => (
     <div className="animate-pulse p-4 border rounded-lg mb-3">
       <div className="flex items-start gap-3">
         <div className="w-10 h-10 bg-gray-200 rounded-full" />
         <div className="flex-1">
           <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
           <div className="h-3 bg-gray-200 rounded w-1/2 mb-2" />
           <div className="h-3 bg-gray-200 rounded w-2/3" />
         </div>
         <div className="w-16 h-6 bg-gray-200 rounded-full" />
       </div>
       <div className="mt-3 space-y-1">
         <div className="h-3 bg-gray-200 rounded" />
         <div className="h-3 bg-gray-200 rounded w-5/6" />
       </div>
     </div>
   );
   ```

4. Add an "AI Analyzing" header during loading:

   ```tsx
   {isAnalyzing && (
     <div className="text-center py-4">
       <div className="inline-flex items-center gap-2 text-blue-600 font-medium mb-4">
         <svg className="animate-spin w-4 h-4" .../>
         <span>AI analyzing Invesco signals...</span>
       </div>
       {[1,2,3,4,5].map(i => <SkeletonCard key={i} />)}
     </div>
   )}
   ```

5. Add a staggered reveal when results appear (each card fades in 100ms apart):
   ```tsx
   // Use CSS animation delay on each result card
   style={{ animationDelay: `${index * 100}ms` }}
   className="animate-fadeIn opacity-0"
   ```
   Add to globals.css:
   ```css
   @keyframes fadeIn {
     from { opacity: 0; transform: translateY(8px); }
     to { opacity: 1; transform: translateY(0); }
   }
   .animate-fadeIn {
     animation: fadeIn 0.3s ease forwards;
   }
   ```

6. Also add skeleton loading to the Salesforce view when it "connects":
   - On initial page load, show 2-3 skeleton signal items for 1 second
   - Then reveal the actual signal data
   - This makes it feel like it's fetching live from Salesforce

7. Run: npm run build — confirm 0 errors.

Report: Files modified, what the loading experience looks like, and mobile behavior.
```

---

## Acceptance Criteria
- [ ] Signal search shows 1.5-2s "AI analyzing..." animation before results
- [ ] Skeleton cards match the shape of actual result cards
- [ ] Results appear with staggered fade-in animation
- [ ] Salesforce view has brief loading state on page mount
- [ ] Animation is smooth on mobile (no jank)
- [ ] Build passes 0 errors
