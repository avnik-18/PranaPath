# WALLET-AND-TEAM-PROCESS.md — no-personal-spend playbook (verified against event rules 2026-10-11)

## A. Safety rails (the "$0 forever" checklist)
1. **Choose the AWS Free Plan at signup** (not the paid "trial"). Nothing can bill, ever; account auto-closes after 6 months — fine for the event.
2. Card step = mandatory ₹2 debit/RuPay verification at AWS signup (event FAQ: debit + RuPay accepted; ~₹2, refunded). NO card means NO new AWS account — there is no cardless signup. A *virtual* RuPay card (bank app → virtual card) works; it does not need to be a credit card. On the Free Plan that ₹2 is the only touch the card ever gets. **Cardless plan-Z** (only if even ₹2 is impossible): AWS Builder Center "free sandboxes — 8-hour environments, no account needed" (event resources list) — usable for experiments, but no stable judge-visible URL, so not our plan A.
3. **Billing → Budgets → $5 budget with email alarm** (first budget is free). Even Free-plan accounts can set it; you get an email at half/100%.
4. Billing console → turn OFF "charges report" noise not needed; ignore — no card = no charge path.
5. Our stack's burn profile (whole event): Lambda ~$0.01 worst case · DynamoDB $0 (on-demand, free tier) · Bedrock Nova a few ₹ in pennies · API GW $0 · Amplify free tier · SNS pennies. **Realistic total <$0.50 even without free tier credits.**
6. After the demo: the advisory (Step Functions + EventBridge) has a kill switch — `APPLY_ENABLED=false` (stack variable) or delete the demo stack (one `delete-stack` command). We wait until film is captured, then decide keep-vs-delete.
7. Quota safety: our usage is tiny vs free quotas; only watch item = Bedrock throttling (handled by fallback template anyway).

## B. Team access (the minimum-friction process)
- AWS account = ONE. There is no separate "team wallet" vs "personal wallet" — credits sit on the account that created them.
- WHO creates it: the leader (captain). With his PHONE — AWS signup works fine in a mobile browser; verification ₹2 from his debit/RuPay.
- The account should ideally be created under a FRESH email (a new Gmail made by the leader in 2 min), NOT anyone's personal mailbox — keeps root clean and no one needs anyone's personal password. **Nobody ever needs another member's Gmail password.**
- Two safe access paths once the account exists:
  - **Path A (leader-only, zero sharing):** the team sends him ONE zip file; he opens his phone browser → AWS console → **CloudShell** → uploads zip → pastes 2 commands from `infra/DEPLOY.md` → copies the output URLs back to chat. Works on phones. Recommended if sharing credentials feels heavy before a deadline.
  - **Path B (full control for the builder):** leader creates an **IAM user** for the builder (name `ecoroute-builder`, console access + temporary password, MFA optional), the builder logs in on their own laptop and runs everything. Standard practice; needs 3 clicks on the leader's phone.

## C. The $25 team credits — exact acquisition steps
1. Every member (including the leader) registers SEPARATELY first: event page (WeMakeDevs account) + builder.aws.com profile with university enrollment (SheerID) — "captain cannot register the rest".
   - **Registering with personal emails is CORRECT and required** — prizes/certificates/fast-track are sent to "the details you registered with". The optional fresh Gmail advice applies ONLY to the AWS root account (hygiene), never to hackathon registration; the two are separate systems and no email mismatch between them breaks anything.
2. The **leader alone** opens the event page → Credits section ($25 card) → fills the claim form → code is issued to registered participants and lands on the registered contact (form/email).
3. He redeems inside the account: AWS console → **Billing → Credits → Redeem credit** → paste code. It attaches to the team account. If the $200 trial credits still remain, rules ask that they be used first — with our pennies-scale burn we likely never even need the $25.
4. If the form needs a "team registration ID", it comes from the leader's own event registration page.

## D. Read-to-the-leader script (phone call, copy verbatim)
> Four things, five minutes, all from your phone:
> 1. Register yourself on the event page AND builder.aws.com (your enrollment verify) — every member must, and rules say I can't do it for you.
> 2. Create our TEAM AWS account with a new Gmail (Free Plan, not paid). ₹2 debit verification. Set MFA — done.
> 3. Open the $25 claim form on the event page (Credits section) and fill it as team leader — one form per team, yours.
> 4. Either make me an IAM user (3 clicks) or just wait for my zip and run two commands in CloudShell from your phone. No Gmail passwords ever — mine or yours.
