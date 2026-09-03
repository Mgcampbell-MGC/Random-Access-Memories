import random, json
random.seed()  # OS entropy

DOMAINS = """music rights|competitive sport|aquaculture and fish farming|tattoo and body art|beekeeping and apiculture|religious institutions and churches|orchestras and classical music|film and television production|scientific instruments and calibration|rare books and manuscripts|seed banks and plant genetics|prisons and correctional services|cruise and passenger shipping|mining and mineral exploration|dance and ballet|horse racing and equestrian sport|wine and viticulture|watchmaking and horology|studio ceramics and glass|university admissions and credentials|fertility, sperm and egg banking|pedigree animal breeding|drones and unmanned aviation|satellites and space services|industrial gases and cryogenics|perfume and fragrance|human hair and wigs|dentistry and dental labs|prosthetics and orthotics|hearing aids and audiology|taxidermy and natural history|museums and collections management|auction houses|pawnbroking and asset lending|self-storage|commercial laundry and textile rental|craft brewing and distilling|commercial greenhouses and horticulture|cemeteries and crematoria|playgrounds and public play equipment|lifts, elevators and escalators|locksmithing and physical security|swimming pools and spas|beauty devices and aesthetics|childcare and nurseries|veterinary practice|scuba diving and marine tourism|climbing and mountaineering|hunting and firearms|fireworks and pyrotechnics|circus and live performance rigging|antiquarian maps and philately|vintage and classic vehicles|marinas and yachting|falconry and working animals|forensic science services|archaeology and heritage compliance|bells, organs and church instruments|orchards and specialty agriculture|salt, ice and cold chain|bespoke tailoring and lastmaking|luthiery and instrument repair|art conservation and restoration|stained glass and architectural salvage|beekeeping equipment|specialty coffee and cacao origin|olive oil and single-origin food|caviar, truffles and luxury food|down, feather and specialty textiles|leather tanning and exotic skins|pearls, gemstones and lapidary""".split('|')

OBJECTS = """a passport|a human tooth|a violin|a customs seal|a soil sample|a tissue block|a hair sample|a rough diamond|a handwritten signature|a fingerprint|a bee colony|a wine bottle|a stretched canvas|a photographic negative|a master audio tape|an injection mould|a stamping die|a shoemaker's last|a paper dress pattern|a physical key|a postage stamp|a coin|a fossil|a meteorite fragment|a seed lot|a frozen embryo|a grafted rootstock|a church bell|an organ pipe|a breeding certificate|a hallmark punch|a calibration weight|a blood tube|a semen straw|a race-day sample|a hive frame|a core drill sample|a film print|a costume|a taxidermy mount|a manuscript folio|a survey monument|a ship's log|an aircraft logbook|a tyre|a firearm|a prosthetic socket|a hearing-aid mould|a dental impression|a cask""".split('|')

JURIS = """Japan|Norway|Portugal|United Arab Emirates|Singapore|Australia|Canada|South Africa|Chile|Argentina|Mexico|Ireland|Netherlands|Switzerland|New Zealand|Israel|South Korea|Poland|Czechia|Uruguay|Paraguay|Colombia|Peru|India|Indonesia|Philippines|Kenya|Nigeria|Morocco|Turkey|Greece|Italy|Spain|Germany|France|United Kingdom|Sweden|Denmark|Finland|Iceland|Malta|Cyprus|Luxembourg|Hong Kong|Taiwan|Thailand|Vietnam|Malaysia|Saudi Arabia|Qatar|Panama|Costa Rica|Ecuador|Bolivia|the European Union as a bloc|a specific US state of your choosing|Brazil itself""".split('|')

MECHANISMS = """a per-transaction fee|a royalty on every resale|an annual attestation fee|a bonded guarantee premium|an escrow holding fee|a membership subscription|a per-batch certificate|a licence to a database|a per-event witness fee|a subscription to a change feed|a deposit-holding fee|a listing fee|a per-unit stamp or seal|a percentage of an insured value|a fee per document certified|a retainer for standing readiness|a fee per sample handled|a per-consignment inspection fee|a flat fee per dispute resolved|a fee to be named as an agent of record|a fee per identity verified|a per-year custodianship fee|a fee per translation certified|a per-lot cataloguing fee|a fee per provenance report|a charge for a witnessed count|a fee per condition report|a percentage of a recovered amount|a fee for holding a physical original|a per-shipment declaration fee""".split('|')

BUYERS = """an insurer|an auction house|a university registrar|a religious institution|a sports federation|a bank's compliance desk|a single family office|a probate or estate lawyer|a museum registrar|a pedigree breeder|a luthier or instrument dealer|a vineyard or winery|a hospital procurement desk|a film studio's rights clearance department|a record label's rights department|a pension fund|an embassy or consulate|a shipping line|a customs broker|a fertility clinic|a laboratory accreditation body|a reinsurer|a certification body|a commodity trader|a jeweller or gemstone dealer|a specialist courier|a bonded warehouse|a franchise network|a professional association|a national sports anti-doping body|a livestock exporter|a seed or plant breeder|an art dealer or gallery|a private bank's collectibles desk|a specialty insurance underwriter|a diagnostics laboratory""".split('|')

hunters = []
# 10 four-dimension collisions
for i in range(10):
    hunters.append({
        "key": f"seed{i+1:02d}",
        "domain": random.choice(DOMAINS),
        "object": random.choice(OBJECTS),
        "juris": random.choice(JURIS),
        "mechanism": random.choice(MECHANISMS),
        "buyer": random.choice(BUYERS),
    })
# 4 single-dimension wide sweeps
for i, dim in enumerate(["domain", "object", "mechanism", "buyer"]):
    src = {"domain": DOMAINS, "object": OBJECTS, "mechanism": MECHANISMS, "buyer": BUYERS}[dim]
    hunters.append({"key": f"wide-{dim}", "single_dim": dim,
                    "values": random.sample(src, 6)})
# 2 pure wildcards
hunters.append({"key": "wildcard-1", "wildcard": True})
hunters.append({"key": "wildcard-2", "wildcard": True})

json.dump(hunters, open("hunters.json", "w"), ensure_ascii=False, indent=1)
for h in hunters:
    if h.get("wildcard"): print(h["key"], "-> PURE WILDCARD")
    elif h.get("single_dim"): print(h["key"], "->", h["single_dim"], ":", "; ".join(h["values"])[:110])
    else: print(h["key"], "->", h["domain"], "|", h["object"], "|", h["juris"], "|", h["mechanism"], "|", h["buyer"])
