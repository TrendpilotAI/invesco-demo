## Task: Print-on-Demand Integration (Printful/Printify)
## Priority: medium
## Effort: 16 hours
## Description:
Allow users to order physical printed copies of their FlipMyEra stories/ebooks as high-quality photo books or hardcovers. Integrate with Printful or Printify API. This is a significant revenue upsell — physical books can sell for $25-50+ with good margins.

## Coding Prompt:
You are implementing print-on-demand for FlipMyEra at /data/workspace/projects/flip-my-era/.

Use Printful API (https://developers.printful.com/docs/) or Printify (https://printify.com/app/account/api).

Steps:
1. Create Supabase Edge Function `supabase/functions/print-order/index.ts`:
   - Accept `{ storyId: string, format: 'photobook_8x8' | 'hardcover_8x11', shippingAddress: Address }`
   - Fetch story content and images from Supabase
   - Format as print-ready PDF using a PDF generation service
   - Submit order to Printful/Printify API
   - Return order tracking info
   - Store order in new `print_orders` DB table

2. Create DB migration `supabase/migrations/XXXX_print_orders.sql`:
   ```sql
   CREATE TABLE print_orders (
     id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
     user_id uuid REFERENCES auth.users NOT NULL,
     story_id uuid NOT NULL,
     provider_order_id text,
     status text DEFAULT 'pending',
     format text NOT NULL,
     shipping_address jsonb,
     price_cents integer,
     created_at timestamptz DEFAULT now()
   );
   ALTER TABLE print_orders ENABLE ROW LEVEL SECURITY;
   CREATE POLICY "Users see own orders" ON print_orders FOR SELECT USING (auth.uid() = user_id);
   ```

3. Create component `src/modules/story/components/PrintOrderButton.tsx`:
   - "Order Physical Copy" button on story view/download page
   - Address form using react-hook-form
   - Format selector with price preview
   - Stripe checkout flow for print orders (one-time payment, not subscription)

4. Add `print_orders` to admin dashboard for fulfillment tracking

5. Gate behind `premium_features` flag initially, then open to all paid tiers

## Acceptance Criteria:
- [ ] User can request physical print from story page
- [ ] Address form validates correctly
- [ ] Order submitted to Printful/Printify and stored in DB
- [ ] User receives confirmation email via Brevo
- [ ] Admin can see all print orders
- [ ] RLS policy restricts users to their own orders

## Dependencies: 010-pending-P1-flip-my-era-wire-gallery-to-supabase.md
