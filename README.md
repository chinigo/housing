# House

## Cover letter

Building a home is the riskiest thing I ever intend to do and I intend to do it only once.

It will require an enormous investment of time, money, sweat, and tears (but hopefully only trace amounts of blood) from
not just me but also the dozens of professionals I'll need to hire. If successful, the yield of that investment is a
lifetime of comfort and security for me and my family — and a remunerative project for those professionals. But there
are infinite ways to fail.

I am no expert, so nothing in this document is set in stone. I look to you, as the expert, to set me straight and help
me to refine this plan, here at the outset and iteratively as we execute it.

All of which is to say, let's plan for change but let's get the big things Right.

The big things are the ones that are hardest/most expensive to change. In "How Buildings Learn," Stewart Brand presents
this list: site, structure, skin (i.e. building envelope), services, space plan, stuff. Those elements — in that order —
are my priorities.

Thank you for your consideration.

## Goals

- House myself and one other adult into our old age.
- High build quality.
  - High-quality, modestly oversized, mechanical systems.
  - High-quality appliances and fixtures.
- Optimize for total lifetime cost of ownership.
  - Prefer lower operating costs to lower construction cost where practical.
  - Prefer systems that are easy to maintain.
  - Highly energy-efficient.
- In case of emergency, core mechanical systems — HVAC, electrical, water, and waste — can be operated off-grid.
- Take advantage of the natural beauty of the site.
- Take advantage of the energy resources available to the site.
  - Most probably this means solar, but also micro-hydro or geothermal if practical.
- Can be upgraded at some point in the future for an adult with mobility issues (either myself or a family member).
  - A person in a wheelchair can access and use:
    - At least one main entryway.
    - A bedroom.
    - A bathroom with usable facilities.
    - The kitchen and dining areas.
    - Other main living areas.
  - Don't need to build these accommodations yet, just need to be *able* to build them in the future.

## Anti-goals

- "McMansion."
  - Square footage for square footage's sake.
  - Attractive but impractical features.
  - (I do want those sweet, high-end appliances, though.)
- Official certification of energy efficiency.
  - I want an energy efficient home, but I don't care about hitting the arbitrary marks required for, e.g., Phius or
    passive house certification.

## Requirements

### Site

- Outside a 500-year flood zone.
- Low risk of wildfire (or mitigation against it with, e.g., a firebreak).
- Some element of natural beauty — a view of water, rolling hills, a valley, etc.
- Has some topography to it, a little vertical elevation.
- Access to reliable water and waste systems.

### Infrastructure & Mechanical Systems

#### Heating/cooling

- Cool entire house to 70°F during the hottest day of the year.

- Heat entire house to 65°F during the coldest day of the year.

- Relatively fine-grained HVAC zones. Would like to be able to selectively heat/cool individual rooms to optimize energy
consumption for my daily living pattern.

- Meet or exceed [BSC's recommended R-values for Climate Zone
  6](https://buildingscience.com/sites/default/files/migrate/pdf/BA-1005_High%20R-Value_Walls_Case_Study.pdf):

   | Element                   | R-value |
   |:--------------------------|:-------:|
   | Slab                      | 10      |
   | Basement walls            | 20      |
   | Exposed floor             | 40      |
   | Walls                     | 40      |
   | Compact or cathedral roof | 60      |
   | Vented Attic              | 70      |

#### Energy

- Sizing:
  - Figure out the max baseline electrical load. (Given the climate, that'll likely be in winter.)
  - Figure out minimum "emergency" load to support off-grid.
    - This is necessarily < 1 of the baseline and would be determined by the minimum acceptable ΔT in an emergency
      (assuming HVAC is the thing that consumes the most energy.)
  - Up to that minimum emergency load, I'm content to *lose money* (within reason) producing energy relative to buying
    it.
  - Between emergency and baseline, I'd like to produce as much energy as possible while remaining *cost-neutral*.
  - Willing to *overproduce* above the baseline if producing energy is *revenue-positive*.
- Practicality of a [smart electrical panel](https://www.span.io/)?

#### Water

- Supply:
  - Free of microbes.
  - Softened to reduce mineral accumulation in fixtures, appliances, and dishware.
  - Low iron content to reduce staining of sinks.
  - Municipal water would be ideal.
- Temperature control:
  - Hot water available within a few seconds (< 10s) of starting tap.
  - Indefinite amount of hot water.
  - Tankless heater with recirculation?
    - How well-insulated can you make the recirculation loop to minimize thermal losses?
    - What is the typical control loop like? Is there a separate setpoint for the recirculation loop, apart from the
      setpoint of the tankless heater itself?
    - Does it use an auxiliary heater or does it feed back through the main tankless heater?
    - I've head tankless heaters "don't like being cycled too frequently." Is that true? Options for hysteresis?
  - [Drain water heat recovery system?](https://www.energy.gov/energysaver/drain-water-heat-recovery)
- Source of filtered, potable water.
  - I really don't care if my shower is filtered, but with the high mineral content in the area, I want my drinking
    water to be.
  - Separate faucet at kitchen sink for filtered, potable water?
  - Or maybe just rely on an in-fridge water filter for this?
  - Is whole house filtering worth it?
    - Feels like the high-volume use cases — shower, toilet, dishwasher, landscaping — don't need filtering and use
      *way* more water than potation. That feels like a waste of filter medium.
- Easy to maintain.
  - Manifold to easily shut off specific branches? Worth the trouble? Compatible with recirculation loop?
  - Copper vs PEX?

#### Waste

- Municipal sewage would be ideal.
- Handle waste for 2 adults.

#### Data and Home Automation

- Can listen to music throughout the house.
  - Can direct audio from any connected source to any speaker zone.
- Security
  - Doors  and windows are wired for security system sensors.
  - Wired for cameras at strategic locations.
  - Motion-activated floodlights at entryways.
  - No external service providers, though. No data leaves the physical premises. I'd rather [cobble together a
    closed-circuit system](https://ipcamtalk.com/wiki/ip-cam-talk-cliff-notes/).
- Can control lights, HVAC, and speakers centrally.
  - [Control4](https://www.control4.com/)?
- Prefer dimmable lights where practical.
- Central server room/closet with dedicated ventilation (maybe even a dedicated HVAC zone).
  - Small-diameter piping to exterior, for plumbing in [an outdoor water chiller
    unit](https://www.rigidhvac.com/store/products/large-power-chiller-kvb150z) in the future to water-cool computer
    components.

### Spaces

#### Shop

##### Activities

- Produce furniture for myself and the home.
- Build computers and other electronics projects.

##### Requirements

- Conditioned space so it can be used year-round.
- Can easily bring 4' x 8' sheet goods into the space.
  - French doors leading into garage?
- Finished, sealed cement floor.

#### Kitchen & Dining

##### Activities

- Cook daily meals for myself.
- Host dinner a few times a month for 4-6 people.
- Host Thanksgiving or Christmas dinner for up to 10 people.

##### Requirements

- Easy to clean.
  - Can mop the floor aggressively - soak and scrub.
    - Floor is resistant to water damage. Neither the floor nor the subfloor should be damaged by the occasional puddle.
  - Counter-tops and backsplashes are easy to scrub down.
- Counter-tops:
  - Resistant to heat damage.
  - Resistant to staining.
  - Material:
    - As I understand it, the main tradeoffs are between resistance to staining, resistance to heat damage, and
      resistance to etching by acids.
    - In the long term, etching feels like it's both the easiest to mitigate against (by regularly sealing the surface)
      and the easiest to repair (by polishing the surface).
    - Is that right?
    - Does that analysis, then, recommend a dense, natural marble instead of a quartz or quartzite?
- Space to grow fresh herbs year-round.
- Sink
  - No lip with countertop. Undermount or flush mount.
  - Material:
    - Resilient against dropped dishes, scraping silverware, thermal shock. Shouldn't chip or crack over time.
    - Non-porous.
    - Easy to clean.
    - Ok, so no porcelain. Stainless steel? What other options are there?
  - Dishwashing
    - Can be stopped up to soak dishes.
    - [Commercial spray faucet.](https://www.webstaurantstore.com/waterloo-prdx-1-15-gpm-deck-mounted-pre-rinse-faucet-with-single-base/750PRDX.html)
    - Area for draining clean dishes.
      - Runnels or a dishdrain ground into the countertop maybe?
  - Potable, filtered water.
    - Either the cold water tap is filtered or there's a separate tap.
  - [This is nice.](https://www.blanco.com/int-en/sinks/subline-f/subline-430-270-u-silgranit-w-o-drain-remote-control-pdp-60.415/?articleNr=523151)
  - Maybe I'm actually describing two sinks? One for food prep and one for dishwashing? Depends on the overall kitchen layout, I guess.
- Stovetop
  - Flush mount.
  - Induction.
  - [This is nice.](https://www.mieleusa.com/e/induction-cooktop-km-6375-no-colour-9775920-p)
- Oven
  - Cabinet style, over-and-under with microwave.
  - [This is nice.](https://www.mieleusa.com/e/30-inch-convection-oven-h-7680-bp-clean-touch-steel-11805550-p)
- Microwave
  - Cabinet style, over-and-under with stove.
  - [This is nice.](https://www.mieleusa.com/e/built-in-microwave-oven-24-width-m-7240-tc-am-clean-touch-steel-11845600-p)
- Refrigerator
  - Cabinet style, side-by-side with freezer.
- Freezer
  - Cabinet style, side-by-side with refrigerator.
- Dishwasher
  - 

#### Living room/Entertainment center

##### Activities

- Watch television/movies/video games in amazing quality.
  - Play audio at arbitrary volume without disturbing neighbors.

##### Requirements

#### Garage

##### Activities

- Store 2 cars.
- Can be upgraded to charge an electric vehicle.

##### Requirements

#### Master Bathroom

##### Activities

- Shower daily.
- Take long, soaking bath a few times a week.
- Stumble in in the middle of the night to urinate.

##### Requirements

- Connected to master bedroom.
  - Not necessarily exclusively accessed via bedroom. Could be open to the rest of the house.
- Super resistent against mold and humidity.
  - Modestly oversized ventilation.
  - Able to keep up with the steam produced by the shower OR bath on running on full blast (not necessarily both at the
    same time).
- Floor:
  - Water resistant.
    - Neither the floor material nor the subfloor should be damaged by the occasional puddle.
  - Easy to clean.
    - Floor drain?
  - Slip resistant.
  - Tile? Slate?
- Wall-mounted toilet.
  - No gross wax seal.
  - Can nevertheless be serviced without ripping open the wall. Tile-able access panel?
  - Electric bidet seat.
- Low-flow urinal.
  - Can be used at the same time as the toilet. (i.e. not right next to the toilet at the height of a seated person's
    head.)
- Shower and/or tub:
  - Can make it super steamy without causing damage.
    - Glass door instead of curtain, so shower stall can be isolated from rest of room?
    - Exhaust fan inside shower stall?
    - Tile all the way up the wall and on the ceiling.
  - Can take long, soaking baths:
    - Either a dedicated tub or a shower/tub combo.
    - Can maintain water temperature indefinitely.
    - Whirlpool tub?
  - Can easily rinse down shower stall walls after bathing.
    - Handheld shower head? Either alone or with other fixtures.
- Lighting
  - Dedicated light in shower stall for good visibility while bathing.
  - High-intensity, dimmable, lighting near vanity for easier grooming.
  - Integrated, low-intensity, motion-activated night lights to illuminate the toilet, urinal, and sink areas.

#### Master Bedroom

#### Office

#### Guest Bedroom

- Doesn't necessarily need to be a discrete room. Could be an alternate usage mode of the office.

#### Living Room

#### Outside

## Aesthetics

## Open Questions

- Is it pragmatic to go full electric? Electric appliances make sense, but what about heating?
- ~~Does the electric utility buy back surplus energy from grid-tied systems?~~
  - National Grid [will convert negative usage to
    cash](https://www9.nationalgridus.com/non_html/Net%20Metering%20FAQ.pdf).
  - Con Edison only [provides statement
    credits](https://www.coned.com/en/save-money/using-private-generation-energy-sources/solar-energy/solar-energy-installation-faq).

## Resources

- [FEMA National Risk Index](https://hazards.fema.gov/nri/data-resources)
- [FEMA fire risk map](https://www.arcgis.com/home/item.html?id=9274dfe5318540d7a09f0117c0be0730)
