#!/usr/bin/env python3
"""
RAPTOR Breadth Calculator
Scarica prezzi da Yahoo Finance e calcola A/D Line, McClellan Oscillator
e Summation Index per STOXX 600, S&P 500, NASDAQ 100, DAX, FTSE 100, IBEX 35, MIB 40.
Output: data/breadth.json
"""

import json, os, time
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf

PERIOD = "1y"   # ~252 giorni lavorativi

# ── Universe ──────────────────────────────────────────────
STOXX_TICKERS = [
    "III.L","A2A.MI","AAK.ST","AALB.AS","ABBN.SW","ABDN.L","ABN.AS","AC.PA",
    "ACKB.BR","ACS.MC","ADEN.SW","ADS.DE","ADM.L","ADYEN.AS","AED.BR","AGN.AS",
    "AENA.MC","ADP.PA","AFRY.ST","AGS.BR","AD.AS","A5G.IR","AF.PA","AI.PA",
    "AIR.PA","AKRBP.OL","AKZA.AS","ALC.SW","ALFA.ST","ALE.WA","ALV.DE","ALLN.SW",
    "ALO.PA","ATE.PA","AMS.MC","AMBU-B.CO","AMP.MI","AMS.SW","AMUN.PA","ANDR.VI",
    "AAL.L","ABI.BR","ANTO.L","MT.AS","ARGX.BR","AKE.PA","AT1.DE","ASHM.L",
    "ASMI.AS","ASML.AS","ASRNL.AS","ASSA-B.ST","G.MI","ABF.L","AZN.L","ATCO-A.ST",
    "ATO.PA","AUTO.L","AV.L","AVOL.SW","CS.PA","BME.L","BA.L","BAMI.MI","SAB.MC",
    "BIR.IR","PEO.WA","BKT.MC","BARC.L","BTRW.L","BARN.SW","BAS.DE","BAYN.DE",
    "BBVA.MC","BEZ.L","BC8.DE","BEI.DE","BEIJB.ST","BEAN.SW","BWY.L","BKG.L",
    "BHP.L","BIM.PA","BMW.DE","BNP.PA","BOL.ST","EN.PA","BP.L","BNR.DE","BATS.L",
    "BLND.L","BT-A.L","BNZL.L","BRBY.L","BVI.PA","CABK.MC","CPR.MI","CAP.PA",
    "AFX.DE","CARL-B.CO","CCL.L","CA.PA","CAST.ST","CDR.WA","CLNX.MC","CNA.L",
    "CLN.SW","CNHI.MI","CCH.L","COFB.BR","COLO-B.CO","CBK.DE","CPG.L","CON.DE",
    "CTEC.L","CRBN.AS","1COV.DE","COV.PA","ACA.PA","CRH.L","CRDA.L","EVD.DE",
    "BN.PA","DANSKE.CO","AM.PA","DSY.PA","DCC.L","DHER.DE","DEMANT.CO","DLN.L",
    "DBK.DE","DB1.DE","DPW.DE","DTE.DE","DGE.L","DIA.MI","DNP.WA","DNB.OL",
    "DSV.CO","EOAN.DE","EDEN.PA","EDP.LS","FGR.PA","ELECTB.ST","EKTA-B.ST",
    "ELI.BR","ELIS.PA","ELISA.HE","EMEIS.PA","EMSN.SW","ENG.MC","ELE.MC",
    "ENEL.MI","ENGI.PA","ENI.MI","ENT.L","EPIROC-A.ST","EQT.ST","EQNR.OL",
    "EBS.VI","EL.PA","ESSITY-B.ST","COLR.BR","RF.PA","ERF.PA","ENX.PA","EVO.ST",
    "EVK.DE","EVT.DE","EXPN.L","FERG.L","RACE.MI","FER.MC","FBK.MI","FHZN.SW",
    "FLTR.L","FORTUM.HE","EO.PA","FNTN.DE","FME.DE","FRE.DE","FRES.L","FPE3.DE",
    "GLPG.BR","GALE.SW","GALP.LS","GBLB.BR","G1A.DE","GEBN.SW","GFC.PA",
    "GMAB.CO","GF.SW","GETI-B.ST","GET.PA","GIVN.SW","GJF.OL","GL9.IR","GLEN.L",
    "GN.CO","GLJ.DE","GRF.MC","SK.PA","GSK.L","HLMA.L","HMSO.L","HNR1.DE",
    "HAS.L","HEIG.DE","HEIA.AS","HEIO.AS","HLE.DE","HFG.DE","HELN.SW","HEN3.DE",
    "HM-B.ST","HER.MI","RMS.PA","HEXA-B.ST","HEXPOL-B.ST","HIK.L","HSX.L",
    "HOLN.SW","HOLM-B.ST","HWDN.L","HSBA.L","BOSS.DE","HUH1V.HE","HUSQ-B.ST",
    "IAG.L","IBE.MC","ICAD.PA","ICG.L","IGG.L","IMCD.AS","IMI.L","IMB.L",
    "INCH.L","ITX.MC","INDU-A.ST","INDT.ST","IFX.DE","INF.L","INGA.AS","COL.MC",
    "IHG.L","IP.MI","ITRK.L","ISP.MI","INVP.L","INVE-B.ST","INW.MI","IPN.PA",
    "ISS.CO","IG.MI","ITV.L","SBRY.L","DEC.PA","JD.L","JDEP.AS","JMT.LS",
    "JMAT.L","BAER.SW","JUP.L","SDC.DE","KBC.BR","KER.PA","KYG.IR","KESKOB.HE",
    "KGH.WA","KGF.L","KRX.IR","KINV-B.ST","KGX.DE","LI.PA","KBX.DE","KNEBV.HE",
    "KPN.AS","KNIN.SW","MMB.PA","LAND.L","LXS.DE","LEG.DE","LGEN.L","LR.PA",
    "LDO.MI","LISP.SW","LLOY.L","ERIC-B.ST","LOGN.SW","LSEG.L","LMP.L","LONN.SW",
    "OR.PA","MC.PA","LHA.DE","LUND-B.ST","MNG.L","EMG.L","MKS.L","MB.MI",
    "MRO.L","MBG.DE","MRK.DE","MRL.MC","ML.PA","MAERSK-B.CO","MONC.MI","MNDI.L",
    "MOWI.OL","MTX.DE","MUV2.DE","NG.L","NTGY.MC","NWG.L","NEL.OL","NEM.DE",
    "NESTE.HE","NESN.SW","NEXI.MI","NXT.L","NIBE-B.ST","NN.AS","NOKIA.HE",
    "TYRES.HE","NDA-FI.HE","NHY.OL","NOVN.SW","NOVO-B.CO","NZYM-B.CO","OERL.SW",
    "OCDO.L","ORSTED.CO","OMV.VI","ORA.PA","ORNBV.HE","ORK.OL","PNDORA.CO",
    "PGHN.SW","PSON.L","PNN.L","RI.PA","PSN.L","PHIA.AS","PIRC.MI","PKN.WA",
    "PKO.WA","PAH3.DE","PST.MI","PSM.DE","PRX.AS","PROX.BR","PRU.L","PRY.MI",
    "PSPN.SW","PUB.PA","PUM.DE","PZU.WA","QIA.DE","QLT.L","RBI.VI","RAND.AS",
    "RKT.L","REC.MI","REE.MC","REL.L","RCO.PA","RNO.PA","RTO.L","REP.MC",
    "RXL.PA","RHM.DE","CFR.SW","RMV.L","RIO.L","ROG.SW","RR.L","ROR.L",
    "RBREW.CO","RS1.L","RUI.PA","RWE.DE","SAAB-B.ST","SAF.PA","SAGA-B.ST",
    "SGE.L","SGO.PA","SPM.MI","SALM.OL","SAMPO.HE","SAND.ST","SAN.PA","SAN.MC",
    "SPL.WA","SAP.DE","SRT3.DE","DIM.PA","SBMO.AS","SCATC.OL","SCHP.SW","SU.PA",
    "SDR.L","SCR.PA","G24.DE","SECU-B.ST","SGRO.L","SESG.PA","SVT.L","SGSN.SW",
    "SHEL.L","SIE.DE","SHL.DE","SIGN.SW","LIGHT.AS","SIKA.SW","WAF.DE","SKA-B.ST",
    "SKF-B.ST","SN.L","SMIN.L","SW.L","SRG.MI","GLE.PA","SW.PA","SOF.BR",
    "SWO.SW","SOI.PA","SOLB.BR","SOON.SW","SOP.PA","SPIE.PA","SPX.L","SSE.L",
    "SSPG.L","STJ.L","SRAIL.SW","STAN.L","STLAM.MI","STM.PA","STERV.HE","STB.OL",
    "STMN.SW","SUBC.OL","SCA-B.ST","SHB-A.ST","UHR.SW","SWED-A.ST","SOBI.ST",
    "SLHN.SW","SPSN.SW","SREN.SW","SCMN.SW","SY1.DE","TEG.DE","TATE.L","TW.L",
    "TECN.SW","FTI.PA","TEL2-B.ST","TIT.MI","TEF.MC","TEL.OL","TEP.PA",
    "TELIA.ST","TEMN.SW","TEN.MI","TRN.MI","TSCO.L","HO.PA","THG.L","TKA.DE",
    "TOM.OL","TTE.PA","TPK.L","TREL-B.ST","BBOX.L","TRYG.CO","TLW.L","UBI.PA",
    "UBSG.SW","UCB.BR","UMI.BR","URW.PA","UCG.MI","ULVR.L","UN01.DE","UTG.L",
    "UTDI.DE","UU.L","UPM.HE","FR.PA","VALMT.HE","VACN.SW","VIE.PA","VER.VI",
    "VWS.CO","VCT.L","DG.PA","VIV.PA","VOD.L","VOE.VI","VOW3.DE","VOLV-B.ST",
    "VNA.DE","VPK.AS","WDP.BR","WRT1V.HE","WEIR.L","MF.PA","SMWH.L","WTB.L",
    "WIE.VI","WKL.AS","WLN.PA","WPP.L","YAR.OL","ZAL.DE","ZURN.SW",
]

SP500_TICKERS = [
    "AAPL","MSFT","NVDA","AVGO","META","GOOGL","GOOG","AMZN","TSLA","CRM",
    "ADBE","INTC","AMD","QCOM","TXN","AMAT","LRCX","KLAC","MU","MRVL","ADI",
    "SNPS","CDNS","FTNT","PANW","CRWD","NOW","WDAY","ADSK","HPQ","HPE","DELL",
    "NTAP","WDC","STX","GLW","TEL","APH","MSI","ZBRA","IT","CTSH","ACN","IBM",
    "ORCL","CSCO","BRK-B","JPM","V","MA","BAC","WFC","GS","MS","C","AXP","BLK",
    "SPGI","MCO","CME","ICE","SCHW","FIS","FI","PYPL","AMP","TROW","AFL","ALL",
    "HIG","MET","PRU","PFG","USB","TFC","COF","CBOE","NDAQ","TRV","JNJ","UNH",
    "LLY","ABBV","MRK","PFE","BMY","ABT","MDT","TMO","DHR","SYK","BSX","ISRG",
    "BDX","A","IDXX","HUM","CVS","CI","ELV","CNC","HCA","MCK","ABC","CAH",
    "REGN","BIIB","GILD","AMGN","VRTX","MRNA","ILMN","HD","NKE","MCD","SBUX",
    "LOW","BKNG","ABNB","MAR","HLT","CCL","RCL","F","GM","APTV","GRMN","HAS",
    "MAT","PVH","TPR","RL","WHR","BBY","DHI","LEN","PHM","ORLY","AZO","GPC",
    "ROST","TJX","DG","DLTR","TGT","WMT","PG","KO","PEP","COST","PM","MO",
    "CL","KMB","GIS","SYY","KR","MKC","HSY","MDLZ","KHC","TSN","CAT","BA",
    "HON","RTX","LMT","NOC","GD","LHX","UPS","FDX","CSX","UNP","NSC","ODFL",
    "DAL","UAL","AAL","WM","RSG","CTAS","CPRT","VRSK","PWR","EME","GE","MMM",
    "XOM","CVX","COP","EOG","DVN","HAL","SLB","VLO","PSX","MPC","WMB","KMI",
    "OKE","EQT","NEE","SO","DUK","D","AEP","EXC","XEL","ETR","ED","AWK","PLD",
    "AMT","CCI","EQIX","PSA","WELL","VTR","O","VICI","SPG","AVB","EQR","ARE",
    "BXP","IRM","DLR","LIN","APD","FCX","NEM","NUE","DOW","LYB","PPG","SHW",
    "PKG","ALB","CF","CTVA","IP","NFLX","DIS","CMCSA","T","VZ","TMUS","CHTR",
    "EA","TTWO","IPG","OMC","TTD","SNAP","PINS","MTCH",
]

NDX_TICKERS = [
    "ADBE","AMD","ABNB","GOOGL","GOOG","AMZN","AMGN","ADI","AAPL","AMAT",
    "ASML","ADSK","ADP","BIIB","BKNG","AVGO","CDNS","CDW","CTAS","CSCO","CTSH",
    "CPRT","COST","CRWD","CSX","DDOG","DXCM","DLTR","EA","EXC","FAST","FTNT",
    "GEHC","GILD","GFS","HON","IDXX","ILMN","INTC","INTU","ISRG","KLAC","KHC",
    "LRCX","LULU","MAR","MRVL","MTCH","MELI","META","MU","MSFT","MRNA","MNST",
    "NFLX","NVDA","NXPI","ORLY","ODFL","ON","PANW","PAYX","PYPL","PEP","PINS",
    "QCOM","REGN","ROST","CRM","NOW","SIRI","SBUX","SNPS","TMUS","TEL","TSLA",
    "TXN","TTD","VRSK","VRTX","WBD","WDAY","XEL","ZM","ZS",
]

# ── Subset nazionali da STOXX (zero fetch aggiuntivi) ──────
DAX_TICKERS  = [t for t in STOXX_TICKERS if t.endswith('.DE')]
FTSE_TICKERS = [t for t in STOXX_TICKERS if t.endswith('.L')]
IBEX_TICKERS = [t for t in STOXX_TICKERS if t.endswith('.MC')]
MIB_TICKERS  = [t for t in STOXX_TICKERS if t.endswith('.MI')]

MARKETS = {
    "stoxx": {"name": "STOXX 600",  "tickers": STOXX_TICKERS},
    "sp500": {"name": "S&P 500",    "tickers": SP500_TICKERS},
    "ndx":   {"name": "NASDAQ 100", "tickers": NDX_TICKERS},
    "dax":   {"name": "DAX",        "tickers": DAX_TICKERS},
    "ftse":  {"name": "FTSE 100",   "tickers": FTSE_TICKERS},
    "ibex":  {"name": "IBEX 35",    "tickers": IBEX_TICKERS},
    "mib":   {"name": "MIB 40",     "tickers": MIB_TICKERS},
}


def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def calc_mcclellan(net_ad: pd.Series):
    e19 = ema(net_ad, 19)
    e39 = ema(net_ad, 39)
    oscillator = e19 - e39
    summation = oscillator.cumsum()
    return oscillator, summation


def fetch_closes(tickers, batch=50, sleep=2):
    """Scarica chiusure in batch per evitare rate limiting."""
    all_closes = {}
    for i in range(0, len(tickers), batch):
        chunk = tickers[i:i+batch]
        print(f"  Downloading {i+1}-{min(i+batch, len(tickers))}/{len(tickers)}...", flush=True)
        try:
            df = yf.download(
                chunk,
                period=PERIOD,
                interval="1d",
                auto_adjust=True,
                progress=False,
                group_by="ticker",
                threads=True,
            )
            if len(chunk) == 1:
                t = chunk[0]
                if "Close" in df.columns:
                    all_closes[t] = df["Close"].dropna()
            else:
                for t in chunk:
                    try:
                        col = df[t]["Close"].dropna()
                        if len(col) > 20:
                            all_closes[t] = col
                    except Exception:
                        pass
        except Exception as e:
            print(f"  Error: {e}", flush=True)
        time.sleep(sleep)
    return all_closes


def build_ad_series(closes_dict):
    """Per ogni data calcola Advancing / Declining / Unchanged."""
    # Allinea tutto su un unico DataFrame
    df = pd.DataFrame(closes_dict)
    df = df.sort_index()

    # Calcola variazioni giornaliere
    ret = df.pct_change()

    adv = (ret > 0.001).sum(axis=1)
    dec = (ret < -0.001).sum(axis=1)
    unc = ret.shape[1] - adv - dec - ret.isna().sum(axis=1)
    net = adv - dec

    # A/D Line cumulativa
    ad_line = net.cumsum()

    # McClellan
    osc, summ = calc_mcclellan(net)

    # Combina in un unico DataFrame
    result = pd.DataFrame({
        "adv": adv.astype(int),
        "dec": dec.astype(int),
        "unc": unc.clip(lower=0).astype(int),
        "net": net.astype(int),
        "ad_line": ad_line.round(1),
        "mcclellan": osc.round(2),
        "summation": summ.round(1),
    }).dropna()

    # Rimuovi le righe iniziali con dati insufficienti (prime 40 righe per EMA39)
    result = result.iloc[40:]

    return result


def df_to_records(df):
    records = []
    for date, row in df.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "adv": int(row["adv"]),
            "dec": int(row["dec"]),
            "unc": int(row["unc"]),
            "net": int(row["net"]),
            "ad_line": float(row["ad_line"]),
            "mcclellan": float(row["mcclellan"]),
            "summation": float(row["summation"]),
        })
    return records


# Mercati che scaricano dati propri
PRIMARY_MARKETS = ["stoxx", "sp500", "ndx"]
# Mercati che riusano i dati STOXX già scaricati (subset per suffisso)
SUBSET_MARKETS  = ["dax", "ftse", "ibex", "mib"]


def main():
    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "markets": {}
    }

    # Cache closes per riutilizzo subset
    closes_cache = {}

    for key, cfg in MARKETS.items():
        print(f"\n=== {cfg['name']} ({len(cfg['tickers'])} tickers) ===", flush=True)

        if key in SUBSET_MARKETS:
            # Filtra dal cache STOXX già scaricato
            stoxx_closes = closes_cache.get("stoxx", {})
            closes = {t: v for t, v in stoxx_closes.items() if t in cfg["tickers"]}
            print(f"  Reusing STOXX cache: {len(closes)} tickers", flush=True)
        else:
            closes = fetch_closes(cfg["tickers"])
            closes_cache[key] = closes
            print(f"  Got data for {len(closes)} tickers", flush=True)

        if len(closes) < 5:
            print(f"  Insufficient data, skipping", flush=True)
            continue

        ad_df = build_ad_series(closes)
        records = df_to_records(ad_df)
        print(f"  {len(records)} days of A/D data", flush=True)

        output["markets"][key] = {
            "name": cfg["name"],
            "ticker_count": len(closes),
            "data": records,
        }

    # Scrivi JSON
    os.makedirs("data", exist_ok=True)
    out_path = "data/breadth.json"
    with open(out_path, "w") as f:
        json.dump(output, f, separators=(",", ":"))

    print(f"\nWritten: {out_path} ({os.path.getsize(out_path)//1024} KB)", flush=True)


if __name__ == "__main__":
    main()
