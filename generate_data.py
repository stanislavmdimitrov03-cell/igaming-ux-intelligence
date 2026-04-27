import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, os

random.seed(42)
np.random.seed(42)
os.makedirs('/home/claude/data', exist_ok=True)

N_PLAYERS = 5000
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)

CHANNELS  = ['paid_search','organic','affiliate','social','referral']
CHANNEL_W = [0.35,0.20,0.25,0.12,0.08]
DEVICES   = ['mobile','desktop','tablet']
DEVICE_W  = [0.62,0.32,0.06]
COUNTRIES = ['UK','DE','FI','NO','SE','IE','AT']
COUNTRY_W = [0.30,0.20,0.15,0.12,0.10,0.08,0.05]
GAME_TYPES= ['slots','live_casino','sports_betting','table_games']
GAME_W    = [0.50,0.25,0.18,0.07]

HOUR_W = np.array([1,1,1,1,1,1,2,3,4,5,6,7,8,8,7,6,6,7,9,10,9,8,5,3],dtype=float)
HOUR_W /= HOUR_W.sum()

def rand_date(start, end):
    return start + timedelta(days=random.randint(0,(end-start).days))

def days_after(base, a, b):
    return base + timedelta(days=random.randint(a,b))

# ── PLAYERS ──────────────────────────────────────────────────────────────────
players = []
for i in range(N_PLAYERS):
    pid     = f'P{i+1:05d}'
    device  = np.random.choice(DEVICES, p=DEVICE_W)
    channel = np.random.choice(CHANNELS, p=CHANNEL_W)
    country = np.random.choice(COUNTRIES, p=COUNTRY_W)
    reg     = rand_date(START_DATE, END_DATE - timedelta(days=60))

    kyc_p   = (0.72 if device=='desktop' else 0.58 if device=='mobile' else 0.65)
    kyc_p  += 0.05 if channel=='affiliate' else 0
    kyc_done= random.random() < kyc_p
    kyc_dt  = days_after(reg,0,3) if kyc_done else None

    ftd_p   = 0.0
    if kyc_done:
        ftd_p = 0.78 if device=='desktop' else 0.61 if device=='mobile' else 0.70
        ftd_p+= 0.06 if channel=='paid_search' else 0
    ftd_done= kyc_done and random.random() < ftd_p
    ftd_dt  = days_after(kyc_dt,0,2) if ftd_done else None
    ftd_amt = round(np.random.lognormal(3.8,0.6),2) if ftd_done else None

    if ftd_done:
        ltv_days  = int(np.random.exponential(45))
        churn_day = min(ltv_days,(END_DATE-ftd_dt).days)
        churned   = churn_day < 60
        total_dep = ftd_amt + (round(np.random.lognormal(4.0,0.7),2)*random.randint(0,8) if not churned else 0)
    else:
        churn_day,churned,total_dep = None,True,0.0

    players.append({'player_id':pid,'registration_date':reg.date(),'country':country,
        'device':device,'channel':channel,'kyc_completed':kyc_done,
        'kyc_date':kyc_dt.date() if kyc_dt else None,
        'ftd_completed':ftd_done,'ftd_date':ftd_dt.date() if ftd_dt else None,
        'ftd_amount':ftd_amt,'total_deposits':round(total_dep,2),
        'churned':churned,'days_active':churn_day})

df_players = pd.DataFrame(players)

# ── SESSIONS ─────────────────────────────────────────────────────────────────
sessions = []
for _, p in df_players[df_players['ftd_completed']].iterrows():
    ftd   = datetime.combine(p['ftd_date'], datetime.min.time())
    days  = max(1, int(p['days_active'] or 1))
    n     = min(300, max(1, int(np.random.poisson(days * 0.4))))
    for _ in range(n):
        dt        = ftd + timedelta(days=random.randint(0, days))
        hour      = int(np.random.choice(range(24), p=HOUR_W))
        is_eve    = hour >= 18
        gtype     = np.random.choice(GAME_TYPES, p=GAME_W)
        dur       = max(2, int(np.random.lognormal(3.0,0.8)))
        bets      = max(1, int(dur * np.random.uniform(1.5,4)))
        stake     = round(np.random.lognormal(1.8,0.9),2)
        nm_p      = 0.28 if gtype=='slots' else 0.15
        nm_cnt    = np.random.binomial(max(1,bets), min(0.99, nm_p*2/max(1,bets)))
        base_ret  = 0.55 if is_eve else 0.40
        returned  = random.random() < min(0.95, base_ret + nm_cnt*0.04)
        rg_flag   = hour < 9 and stake > 20 and dur > 45
        sessions.append({'session_id':f'S{len(sessions)+1:07d}','player_id':p['player_id'],
            'session_date':dt.date(),'hour_of_day':hour,'is_evening':is_eve,
            'game_type':gtype,'duration_mins':dur,'bets_placed':bets,'avg_stake':stake,
            'near_miss_count':nm_cnt,'returned_next_day':returned,'rg_flag':rg_flag,
            'device':p['device']})

df_sessions = pd.DataFrame(sessions)

# ── AGGREGATES ───────────────────────────────────────────────────────────────
total=len(df_players); kyc=df_players['kyc_completed'].sum(); ftd=df_players['ftd_completed'].sum()
ret30=df_players[df_players['ftd_completed']&(df_players['days_active']>=30)].shape[0]

df_funnel=pd.DataFrame([
    {'stage':'1. Registered','players':total,'drop_pct':0},
    {'stage':'2. KYC Completed','players':int(kyc),'drop_pct':round((1-kyc/total)*100,1)},
    {'stage':'3. First Deposit','players':int(ftd),'drop_pct':round((1-ftd/kyc)*100,1)},
    {'stage':'4. Retained 30d','players':int(ret30),'drop_pct':round((1-ret30/ftd)*100,1)},
])

df_nm=df_sessions.copy()
df_nm['nm_bucket']=pd.cut(df_nm['near_miss_count'],bins=[-1,0,2,5,10,999],labels=['0','1-2','3-5','6-10','10+'])
df_nm_agg=df_nm.groupby('nm_bucket',observed=True).agg(sessions=('session_id','count'),avg_return=('returned_next_day','mean')).reset_index()

df_channel=df_players.groupby('channel').agg(registered=('player_id','count'),kyc_done=('kyc_completed','sum'),ftd_done=('ftd_completed','sum'),avg_ftd=('ftd_amount','mean')).reset_index()
df_channel['kyc_rate']=(df_channel['kyc_done']/df_channel['registered']*100).round(1)
df_channel['ftd_rate']=(df_channel['ftd_done']/df_channel['kyc_done']*100).round(1)
df_channel['avg_ftd']=df_channel['avg_ftd'].round(2)

df_device=df_players.groupby('device').agg(registered=('player_id','count'),kyc_rate=('kyc_completed','mean'),ftd_rate=('ftd_completed','mean')).reset_index()
df_device['kyc_rate']=(df_device['kyc_rate']*100).round(1)
df_device['ftd_rate']=(df_device['ftd_rate']*100).round(1)

df_rg=df_sessions.groupby('hour_of_day').agg(sessions=('session_id','count'),rg_flags=('rg_flag','sum'),avg_stake=('avg_stake','mean'),avg_duration=('duration_mins','mean')).reset_index()
df_rg['rg_rate']=(df_rg['rg_flags']/df_rg['sessions']*100).round(2)

# Save
df_players.to_csv('/home/claude/data/players.csv',index=False)
df_sessions.to_csv('/home/claude/data/sessions.csv',index=False)
df_funnel.to_csv('/home/claude/data/funnel.csv',index=False)
df_nm_agg.to_csv('/home/claude/data/near_miss_analysis.csv',index=False)
df_channel.to_csv('/home/claude/data/channel_funnel.csv',index=False)
df_device.to_csv('/home/claude/data/device_conversion.csv',index=False)
df_rg.to_csv('/home/claude/data/rg_by_hour.csv',index=False)

print("✅ All files generated")
print(f"Players:  {len(df_players):,}  |  Sessions: {len(df_sessions):,}")
print("\n── Funnel ──")
print(df_funnel.to_string(index=False))
print("\n── Near-Miss → Return Rate ──")
print(df_nm_agg.to_string(index=False))
print("\n── Device Conversion ──")
print(df_device.to_string(index=False))
print("\n── Channel ──")
print(df_channel[['channel','registered','kyc_rate','ftd_rate','avg_ftd']].to_string(index=False))
print("\n── Top RG Flag Hours ──")
print(df_rg.nlargest(5,'rg_rate')[['hour_of_day','rg_rate','avg_stake']].to_string(index=False))
