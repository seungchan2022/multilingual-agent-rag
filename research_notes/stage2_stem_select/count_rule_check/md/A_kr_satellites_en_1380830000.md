# Coordinated Universal Time

Coordinated Universal Time (UTC) is the primary time standard globally used to regulate clocks and time. It establishes a reference for the current time, forming the basis for civil time and time zones. UTC facilitates international communication, navigation, scientific research, and commerce.

UTC has been widely embraced by most countries and is the effective successor to Greenwich Mean Time (GMT) in everyday usage and common applications. In specialised domains such as scientific research, navigation, and timekeeping, other standards, such as UT1 and International Atomic Time (TAI), are also used alongside UTC.

UTC is based on TAI (International Atomic Time, abbreviated from its French name, temps atomique international), which is a weighted average of hundreds of atomic clocks worldwide. UTC is currently within about one second of mean solar time at 0° longitude, the currently used prime meridian, and is not adjusted for daylight saving time.

The coordination of time and frequency transmissions around the world began on 1 January 1960. UTC was first officially adopted as a standard in 1963 and "UTC" became the official abbreviation of Coordinated Universal Time in 1967. The current version of UTC is defined by the International Telecommunication Union.

Since adoption, UTC has been adjusted several times, notably adding leap seconds from 1972 to 2016. Recent years have seen significant developments in the realm of UTC, particularly in discussions about eliminating leap seconds from the timekeeping system because leap seconds occasionally disrupt timekeeping systems worldwide. In 2022, the General Conference on Weights and Measures adopted a resolution to alter UTC with a new system that would eliminate leap seconds by 2035. This was followed in 2026 by another resolution to officially transition to "continuous UTC" and avoid any further leap seconds, effective May 20, 2027. Since no leap seconds were scheduled at that time, in practical terms the change was effective immediately.

## Etymology

The official abbreviation for Coordinated Universal Time is UTC. This abbreviation comes as a result of the International Telecommunication Union and the International Astronomical Union wanting to use the same abbreviation in all languages. The compromise that emerged was UTC, which conforms to the pattern for the abbreviations of the variants of Universal Time (UT0, UT1, UT2, UT1R, etc.).

McCarthy described the origin of the abbreviation:

In 1967 the CCIR adopted the names Coordinated Universal Time and Temps Universel Coordonné for the English and French names with the acronym UTC to be used in both languages. The name "Coordinated Universal Time (UTC)" was approved by a resolution of IAU Commissions 4 and 31 at the 13th General Assembly in 1967 (Trans. IAU, 1968).

## Uses

Time zones around the world are expressed using positive, zero, or negative offsets from UTC, as in the list of time zones by UTC offset.

The westernmost time zone uses UTC−12, being twelve hours behind UTC; the easternmost time zone uses UTC+14, being fourteen hours ahead of UTC. In 1995, the island nation of Kiribati moved those of its atolls in the Line Islands from UTC−10 to UTC+14 so that the islands and atolls of Kiribati would all be on the same day.

UTC is used in many Internet and World Wide Web standards. The Network Time Protocol (NTP), designed to synchronise the clocks of computers over the Internet, transmits time information from the UTC system. If only milliseconds precision is needed, clients can obtain the current UTC from a number of official internet UTC servers. For sub-microsecond precision, clients can obtain the time from satellite signals.

UTC is also the time standard used in aviation, e.g. for flight plans and air traffic control. In this context it is frequently referred to as Zulu time, as described below. Weather forecasts and maps all use UTC to avoid confusion about time zones and daylight saving time. The International Space Station also uses UTC as a time standard.

Amateur radio operators often schedule their radio contacts in UTC, because transmissions on some frequencies can be picked up in many time zones.

## Mechanism

UTC divides time into days, hours, minutes, and seconds. Days are conventionally identified using the Gregorian calendar, but Julian day numbers can also be used. Each day contains 24 hours and each hour contains 60 minutes. The number of seconds in a minute is normally 60, but from 1972 to 2016, at the insertion of an occasional leap second, it may have instead been 61. Thus, in the UTC time scale, the second and all smaller time units (millisecond, microsecond, etc.) are of constant duration, but the minute and all larger time units (hour, day, week, etc.) are of variable duration. It was not possible to predict the leap seconds far in advance due to the unpredictable rate of the rotation of Earth.

Nearly all UTC days contain exactly 86,400 SI seconds with exactly 60 seconds in each minute. As of 2026 UTC is within about one second of mean solar time (such as UT1) at 0° longitude, (at the IERS Reference Meridian). The mean solar day is slightly longer than 86,400 SI seconds. From 1972 to 2017, occasionally the last minute of a UTC day was adjusted to have 61 seconds. The extra second was called a leap second. It accounted for the accumulated total discrepancy of all the mean solar days since the previous leap second (on average 2 milliseconds per day). Before leap seconds were discontinued, the last minute of a UTC day was theoretically permitted to contain 59 seconds to cover the possibility of the Earth rotating faster, but that was never necessary. The irregular day lengths mean fractional Julian days did not work properly with UTC while leap seconds were in force.

Since 1972, UTC may be calculated by subtracting the accumulated leap seconds from International Atomic Time (TAI), which is a coordinate time scale tracking notional proper time on the rotating surface of the Earth (the geoid). In order to maintain a close approximation to UT1, UTC occasionally had discontinuities where it changed from one linear function of TAI to another. These discontinuities took the form of leap seconds implemented by a UTC day of irregular length. Discontinuities in UTC occurred only at the end of June or December. The International Earth Rotation and Reference Systems Service (IERS) tracks and publishes the difference between UTC and Universal Time, DUT1 = UT1 − UTC.

As with TAI, UTC is only known with the highest precision in retrospect. Users who require an approximation in real time must obtain it from a time laboratory, which disseminates an approximation using techniques such as GPS or radio time signals. Such approximations are designated UTC(k), where k is an abbreviation for the time laboratory. The time of events may be provisionally recorded against one of these approximations; later corrections may be applied using the International Bureau of Weights and Measures (BIPM) monthly publication of tables of differences between canonical TAI/UTC and TAI(k)/UTC(k) as estimated in real-time by participating laboratories. (See the article on International Atomic Time for details.)

Because of time dilation, a standard clock not on the geoid, or in rapid motion, will not maintain synchronicity with UTC. Therefore, telemetry from clocks with a known relation to the geoid is used to provide UTC when required, on locations such as those of spacecraft.

It is impossible to compute the exact time interval elapsed between two UTC timestamps without consulting a table showing how many leap seconds occurred during that interval. Therefore, many scientific applications that require precise measurement of long (multi-year) intervals use TAI instead. TAI is also commonly used by systems that cannot handle leap seconds. GPS time always remains exactly 19 seconds behind TAI (neither system wer affected by the leap seconds introduced in UTC).

October 2026 Resolution 5 of the 28th CGPM (2026) formally implemented Resolution 4 27th CGPM (2022) "On the use and future development of UTC" deciding that;

- Continuous UTC will become effective on 20 May 2027

- The maximum value for the difference |UT1-UTC| will be 3 600 seconds (1 hour), ensuring the long term continuity for UTC for several centuries.

### Time zones

Time zones are usually defined as differing from UTC by an integer number of hours, although the laws of each jurisdiction would have to be consulted if sub-second accuracy were required. Several jurisdictions have established time zones that differ by an odd number of half-hours or quarter-hours from UT1 or UTC.

Current civil time in a particular time zone can be determined by adding or subtracting the number of hours and minutes specified by the UTC offset, which ranges from UTC−12:00 in the west to UTC+14:00 in the east (see List of UTC offsets).

The time zone using UTC is sometimes denoted UTC+00:00 or by the letter Z—a reference to the equivalent nautical time zone (GMT), which has been denoted by a Z since about 1950. Time zones were identified by successive letters of the alphabet and the Greenwich time zone was marked by a Z as it was the point of origin. The letter also refers to the "zone description" of zero hours, which has been used since 1920 (see time zone history). Since the NATO phonetic alphabet word for Z is "Zulu", UTC is sometimes known as "Zulu time". This is especially true in aviation, where "Zulu" is the universal standard. This ensures that all pilots, regardless of location, are using the same 24-hour clock, thus avoiding confusion when flying between time zones. See the list of military time zones for letters used in addition to Z in qualifying time zones other than Greenwich.

On electronic devices which only allow the time zone to be configured using maps or city names, UTC can be selected indirectly by selecting cities such as Accra in Ghana or Reykjavík in Iceland as they are always on UTC and do not currently use daylight saving time (which Greenwich and London do, and so could be a source of error).

### Daylight saving time

UTC does not change with a change of seasons, but local time or civil time may change if a time zone jurisdiction observes daylight saving time (summer time). For example, local time on the east coast of the United States is five hours behind UTC during winter, but four hours behind while daylight saving is observed there.

### Timing centres

There are over 70 official UTC timing centres who maintain atomic clocks around the world from which UTC is calculated. UTC is calculated by the BIPM using weighted averages of the reports by the timing centres. BIPM lists the time differences between the UTC timing centres in a monthly publication called Circular T, which contains the most up to date list of contributors to UTC.

UTC timing centres

| Acronym | Name | Country | City | Former acronym | CIPM MRA signatory | Start year | Stop year |
|---|---|---|---|---|---|---|---|
| AGGO | Argentinian-German Geodetic Observatory | Argentina | La Plata | TCC |  | 2002 |  |
| AOS | Astrogeodynamical Observatory, Space Research Centre P.A.S. | Poland | Borówiec |  |  | 1988 |  |
| APL | Applied Physics Laboratory | United States | Laurel |  |  | 1978 |  |
| AUS | National Measurement Institute | Australia | Sydney |  | NMIA | 1973 |  |
| AZ | Azerbaijan Metrology Institute | Azerbaijan | Baku |  | AzMI | 2025 |  |
| BEV | Bundesamt für Eich- und Vermessungswesen | Austria | Vienna |  | BEV | 1975 |  |
| BFKH | Government Office of Capital City of Budapest, Metrology and Technical Supervisory Department | Hungary | Budapest | MKEH | BFKH | 1974 |  |
| BIM | Bulgarian Institute of Metrology | Bulgaria | Sofia | NMC | BIM | 1991 |  |
| BIRM | Beijing Institute of Radio Metrology and Measurement | China | Beijing |  |  | 1995 |  |
| BOM | Bureau of Metrology of Macedonia | North Macedonia | Skopje |  | BOM | 2017 |  |
| BSJ | Bureau of Standards Jamaica | Jamaica | Kingston |  | BSJ | 2024 |  |
| BY | Belarusian State Institute of Metrology | Belarus | Minsk |  | BelGIM | 2007 |  |
| CAO | Stazione Astronomica di Cagliari (Cagliari Astronomical Observatory) | Italy | Cagliari |  |  | 1982 |  |
| CH | Federal Institute of Metrology (METAS) | Switzerland | Bern |  | METAS | 1972 |  |
| CNES | Centre National d'Etudes Spatiales | France | Toulouse |  |  | 2016 |  |
| CNM | Centro Nacional de Metrologia | Mexico | Querétaro |  | CENAM | 1996 |  |
| CNMP | Centro Nacional de Metrología de Panamá (CENAMEP) | Panama | Panama City |  | CENAMAP AIP | 2003 |  |
| DFM | Dansk Fundamental Metrologi (DFM A/S) | Denmark | Hørsholm |  | DFM | 2022 |  |
| DFNT | Laboratoire de Métrologie de la Direction Générale des Transmissions et de l'Informatique (DEF-NAT) | Tunisia | Tunis |  | DEF-NAT | 2014 |  |
| DLR | Deutsches Zentrum für Luft - und Raumfahrt (German Aerospace Centre) | Germany | Oberpfaffenhofen |  |  | 1996 |  |
| DMDM | Directorate of Measures and Precious Metals | Serbia | Belgrade |  | ZMDM | 1983 |  |
| DTAG | Deutsche Telekom AG | Germany | Frankfurt |  |  | 1981 |  |
| EIM | Hellenic Institute of Metrology | Greece | Thessaloniki |  | EIM | 2007 |  |
| ESA | European Space Agency | Netherlands | Noordwijk | ESTC | ESA | 2012 |  |
| HKO | Hong Kong Observatory | Hong Kong (China) | Hong Kong |  |  | 2004 |  |
| IBM | Instituto Boliviano De Metrologia | Bolivia | La Paz |  | IBMETRO | 2023 |  |
| ICE | Laboratorio Costarricense de Metrologia | Costa Rica | San José |  | LAMETRO-ICE | 2017 |  |
| IDN | Standardization Agency of Indonesia | Indonesia | Jakarta | KIM | SNSU-BSN | 2008 |  |
| IFAG | Bundesamt für Kartographie und Geodäsie (Federal Agency for Cartography and Geodesy) | Germany | Bad Kötzting-Wettzell |  |  | 1988 |  |
| IFZG | State Office for Metrology | Croatia | Zagreb |  | DZM | 2024 |  |
| IGNA | Instituto Geográfico Nacional | Argentina | Buenos Aires |  |  | 1969 |  |
| IMBH | Institute of Metrology of Bosnia and Herzegovina | Bosnia and Herzegovina | Sarajevo |  | IMBIH | 2015 |  |
| INCP | Instituto Nacional de Calidad (INACAL) of Peru | Peru | Lima |  | INACAL | 2016 |  |
| INM | Instituto Nacional de Metrología of Colombia | Colombia | Bogotá |  | INM(CO) | 2017 |  |
| INPL | National Physical Laboratory of Israel | Israel | Jerusalem |  | INPL | 1988 |  |
| INTI | Instituto Nacional de Tecnología Industrial | Argentina | Buenos Aires |  | INTI | 2008 |  |
| INXE | National Institute for Metrology, Quality and Technology (INMETRO) | Brazil | Rio de Janeiro |  | INMETRO | 2012 |  |
| IPQ | Instituto Portugues da Qualidade | Portugal | Caparica |  | IPQ | 1995 |  |
| IT | Istituto Nazionale di Ricerca Metrologica (INRIM) | Italy | Turin | IEN | INRIM | 1970 |  |
| JATC | Joint Atomic Time Commission | China | Lintong |  |  | 1988 |  |
| JV | Justervesenet | Norway | Kjeller |  | JV | 2003 |  |
| KEBS | Kenya Bureau of Standards | Kenya | Nairobi |  | KEBS | 2012 | 2019 |
| KRIS | Korea Research Institute of Standards and Science (KRISS), | South Korea | Daejeon | KSRI | KRISS | 1988 |  |
| KZ | Kazakhstan Institute of Standardization and Metrology | Kazakhstan | Astana |  | KazStandard | 2008 |  |
| LDS | University of Leeds | United Kingdom | Leeds |  |  | 1991 | 2009 |
| LRTE | Laboratório de Referência de Tempo e Espaço | Brazil | São Carlos |  |  | 2018 |  |
| LT | Center for Physical Sciences and Technology (VMT/FTMC) | Lithuania | Vilnius |  | FTMC | 2001 |  |
| LUX | Bureau Luxembourgeois de Métrologie (ILNAS) | Luxembourg | Belvaux |  | ILNAS | 2018 |  |
| LV | Latvian National Metrology Centre | Latvia | Riga |  | LATMB | 2007 | 2021 |
| MASM | Mongolian Agency for Standardization and Metrology | Mongolia | Ulaanbaatar |  | MASM | 2013 |  |
| MBM | Bureau of Metrology - Laboratory for time and frequency | Montenegro | Podgorica |  | BMM | 2014 |  |
| MIKE | VTT Technical Research Centre of Finland Ltd, Centre for Metrology | Finland | Espoo |  | MIKES | 1978 |  |
| MSL | Measurement Standards Laboratory | New Zealand | Lower Hutt |  | MSL | 1984 |  |
| MTC | MAKKAH Time Centre - King Abdulah Centre for Crescent Observations and Astronomy | Saudi Arabia | Makkah |  |  | 2012 |  |
| NAO | National Astronomical Observatory | Japan | Mizusawa | NAOM |  | 1969 |  |
| NICT | National Institute of Information and Communications Technology | Japan | Tokyo | CRL | NICT | 1969 |  |
| NIM | National Institute of Metrology | China | Beijing |  | NIM | 1980 |  |
| NIMB | National Institute of Metrology | Romania | Bucharest |  | INM | 2002 |  |
| NIMT | National Institute of Metrology (Thailand) | Thailand | Pathumthani |  | NIMT | 2001 |  |
| NIS | National Institute for Standards | Egypt | Cairo |  | NIS | 1972 |  |
| NIST | National Institute of Standards and Technology | United States | Boulder | NBS | NIST | 1969 |  |
| NMIJ | National Metrology Institute of Japan | Japan | Tsukuba | NRLM | NMIJ AIST | 1980 |  |
| NMLS | National Metrology Laboratory of SIRIM Berhad | Malaysia | Sepang |  | NMIM | 2002 |  |
| NPL | National Physical Laboratory | United Kingdom | Teddington |  | NPL | 1969 |  |
| NPLI | National Physical Laboratory | India | New Delhi |  | NPLI | 1988 |  |
| NRC | National Research Council of Canada | Canada | Ottawa |  | NRC | 1969 |  |
| NRL | United States Naval Research Laboratory | United States | Washington, D.C. |  |  | 2007 |  |
| NSAI | National Standards Authority of Ireland's National Metrology Laboratory (NSAI NML) | Ireland | Dublin |  | NSAI NML | 2020 |  |
| NTSC | National Time Service Center of China | China | Lintong | CSAO |  | 1980 |  |
| ONBA | Observatorio Naval | Argentina | Buenos Aires |  |  | 1970 |  |
| ONRJ | Observatório Nacional | Brazil | Rio de Janeiro |  | ON/DSHO | 1972 |  |
| OP | Observatoire de Paris/Laboratoire Temps Espace | France | Paris | LPTF, LNE-SYRTE | LNE-OP | 1968 |  |
| KSB/ORB | Koninklijke Sterrenwacht van België/Observatoire Royal de Belgique | Belgium | Brussels |  |  | 1972 |  |
| PL | Consortium of laboratories in Poland | Poland | Warsaw | GUM | GUM | 1977 |  |
| PTB | Physikalisch-Technische Bundesanstalt | Germany | Braunschweig |  | PTB | 1968 |  |
| ROA | Real Instituto y Observatorio de la Armada | Spain | San Fernando | OMSF | ROA | 1989 |  |
| SASO | Saudi Standards, Metrology and Quality Organization | Saudi Arabia | Riyadh |  | SASO-NMCC | 2013 |  |
| SCL | Standards and Calibration Laboratory | Hong Kong (China) | Hong Kong |  | SCL | 1996 |  |
| SG | National Metrology Centre - Agency for Science, Technology and Research (A*STAR) | Singapore | Singapore | PSB | NMC, A*STAR | 1981 |  |
| SIQ | Slovenian Institute of Quality and Metrology | Slovenia | Ljubljana |  | MIRS/SIQ/Metrology | 2007 |  |
| SL | Measurement Units, Standards and Services Department (MUSSD) | Sri Lanka | Colombo |  | MUSSD | 2018 |  |
| SMD | Metrology Division of the Quality and Safety Department - Scientific Metrology | Belgium | Brussels |  | SMD | 2009 |  |
| SMU | Slovenský metrologický ústav (Slovak Institute of Metrology) | Slovakia | Bratislava |  | SMU | 1998 |  |
| SP | Research Institutes of Sweden AB (RISE) | Sweden | Borås |  | RISE | 1978 |  |
| SU | Russian metrological institute of technical physics and radio engineering (FSUE VNIIFTRI") " | Russia | Moskva |  | VNIIFTRI | 1969 |  |
| TL | Telecommunication Laboratories | Taiwan | Zhongli |  | TL | 1972 |  |
| TP | Institute of Photonics and Electronics, Czech Academy of Sciences (IPE/ASCR) | Czech Republic | Praha |  | IPE/ASCR | 1968 |  |
| TUG | Technische Universität | Austria | Graz |  |  | 1977 | 2000 |
| UA | National Scientific Centre Institute of Metrology"" | Ukraine | Kharkiv |  | NSC IM | 2006 |  |
| UAE | Emirates Metrology Institute (EMI/UAE) | United Arab Emirates | Abu Dhabi |  | EMI | 2017 |  |
| UME | Ulusai Metroloji Enstitüsü, Marmara Research Centre, (National Metrology Institute) | Turkey | Gebze-Kocaeli |  | UME | 1994 |  |
| USNO | United States Naval Observatory | United States | Washington, D.C. |  |  | 1968 |  |
| UTE | Administración Nacional de Usinas y Transmisiones | Uruguay | Montevideo |  | UTE | 2023 | 2024 |
| UZ | Uzbek National Institute of Metrology of Uzstandard Agency | Uzbekistan | Tashkent |  | UzNIM | 2023 |  |
| VMI | Vietnam Metrology Institute | Vietnam | Hanoi |  | VMI-STAMEQ | 2008 |  |
| VSL | VSL, Dutch Metrology Institute | Netherlands | Delft |  | VSL | 1973 |  |
| ZA | National Metrology Institute of South Africa (NMISA) | South Africa | Pretoria | CSIR | NMISA | 1972 |  |

## History

In 1928, the term Universal Time (UT) was introduced by the International Astronomical Union to refer to GMT, with the day starting at midnight. Until the 1950s, broadcast time signals were based on UT, and hence on the rotation of the Earth.

In 1955, the caesium atomic clock was invented. This provided a form of timekeeping that was both more stable and more convenient than astronomical observations. In 1956, the U.S. National Bureau of Standards and U.S. Naval Observatory started to develop atomic frequency time scales; by 1959, these time scales were used in generating the WWV time signals, named for the shortwave radio station that broadcasts them. In 1960, the U.S. Naval Observatory, the Royal Greenwich Observatory, and the UK National Physical Laboratory coordinated their radio broadcasts so that time steps and frequency changes were coordinated, and the resulting time scale was informally referred to as "Coordinated Universal Time".

In a controversial decision, the frequency of the signals was initially set to match the rate of UT, but then kept at the same frequency by the use of atomic clocks and deliberately allowed to drift away from UT. When the divergence grew significantly, the signal was phase shifted (stepped) by 20 ms to bring it back into agreement with UT. Twenty-nine such steps were used before 1960.

In 1958, data was published linking the frequency for the caesium transition, newly established, with the ephemeris second. The ephemeris second is a unit in the system of time that, when used as the independent variable in the laws of motion that govern the movement of the planets and moons in the Solar System, enables the laws of motion to accurately predict the observed positions of Solar System bodies. Within the limits of observable accuracy, ephemeris seconds are of constant length, as are atomic seconds. This publication allowed a value to be chosen for the length of the atomic second that would accord with the celestial laws of motion.

The coordination of time and frequency transmissions around the world began on 1 January 1960. UTC was first officially adopted in 1963 as CCIR Recommendation 374, Standard-Frequency and Time-Signal Emissions, and "UTC" became the official abbreviation of Coordinated Universal Time in 1967.

In 1961, the Bureau International de l'Heure began coordinating the UTC process internationally (but the name Coordinated Universal Time was not formally adopted by the International Astronomical Union until 1967). From then on, there were time steps every few months, and frequency changes at the end of each year. The jumps increased in size to 0.1 seconds. This UTC was intended to permit a very close approximation to UT2.

In 1967, the SI second was redefined in terms of the frequency supplied by a caesium atomic clock. The length of second so defined was practically equal to the second of ephemeris time. This was the frequency that had been provisionally used in TAI since 1958. It was soon decided that having two types of second with different lengths, namely the UTC second and the SI second used in TAI, was a bad idea. It was thought better for time signals to maintain a consistent frequency, and that this frequency should match the SI second. Thus it would be necessary to rely on time steps alone to maintain the approximation of UT. This was tried experimentally in a service known as "Stepped Atomic Time" (SAT), which ticked at the same rate as TAI and used jumps of 0.2 seconds to stay synchronised with UT2.

There was also dissatisfaction with the frequent jumps in UTC (and SAT). In 1968, Louis Essen, the inventor of the caesium atomic clock, and G. M. R. Winkler both independently proposed that steps should be of 1 second only. to simplify future adjustments. This system was eventually approved as leap seconds in a new UTC in 1970 and implemented in 1972, along with the idea of maintaining the UTC second equal to the TAI second. This CCIR Recommendation 460 "stated that (a) carrier frequencies and time intervals should be maintained constant and should correspond to the definition of the SI second; (b) step adjustments, when necessary, should be exactly 1 s to maintain approximate agreement with Universal Time (UT); and (c) standard signals should contain information on the difference between UTC and UT."

As an intermediate step at the end of 1971, there was a final irregular jump of exactly 0.107758 TAI seconds, making the total of all the small time steps and frequency shifts in UTC or TAI during 1958–1971 exactly ten seconds, so that 1 January 1972 00:00:00 UTC was 1 January 1972 00:00:10 TAI exactly, and a whole number of seconds thereafter. At the same time, the tick rate of UTC was changed to exactly match TAI. UTC also started to track UT1 rather than UT2. Some time signals started to broadcast the DUT1 correction (UT1 − UTC) for applications requiring a closer approximation of UT1 than UTC provided.

The current version of UTC is defined by International Telecommunication Union Recommendation (ITU-R TF.460-6), Standard-frequency and time-signal emissions, and is based on International Atomic Time (TAI) with leap seconds added at irregular intervals to compensate for the accumulated difference between TAI and time measured by Earth's rotation. Leap seconds are inserted as necessary to keep UTC within 0.9 seconds of the UT1 variant of universal time. See § Current number of leap seconds for the number of leap seconds inserted to date.

### Current number of leap seconds

The first leap second occurred on 30 June 1972 and the last on 31 December 2016. Leap seconds occurred on average about once every 19 months, always on 30 June or 31 December. There were 27 leap seconds in total, all positive, putting UTC 37 seconds behind TAI.

A study published in March 2024 in Nature found that accelerated melting of ice in Greenland and Antarctica due to climate change has slowed Earth's rotation enough to delay the next negative leap-second adjustment to UTC, postponing problems for computer systems.

## Rationale

Earth's rotational speed is very slowly decreasing because of tidal deceleration; this increases the length of the mean solar day. The length of the SI second was calibrated on the basis of the second of ephemeris time and can now be seen to have a relationship with the mean solar day observed between 1750 and 1892, analysed by Simon Newcomb. As a result, the SI second is close to ⁠1/86400⁠ of a mean solar day in the mid‑19th century. In earlier centuries, the mean solar day was shorter than 86,400 SI seconds, and in more recent centuries it is longer than 86,400 seconds. Near the end of the 20th century, the length of the mean solar day (also known simply as "length of day" or "LOD") was approximately 86,400.0013 s. For this reason, UT is now "slower" than TAI by the difference (or "excess" LOD) of 1.3 ms/day.

The excess of the LOD over the nominal 86,400 s accumulates over time, causing the UTC day, initially synchronised with the mean sun, to become desynchronised and run ahead of it. Near the end of the 20th century, with the LOD at 1.3 ms above the nominal value, UTC ran faster than UT by 1.3 ms per day, getting a second ahead roughly every 800 days. Thus, leap seconds were inserted at approximately this interval, retarding UTC to keep it synchronised in the long term. The actual rotational period varies on unpredictable factors such as tectonic motion and has to be observed, rather than computed.

Just as adding a leap day every four years does not mean the year is getting longer by one day every four years, the insertion of a leap second every 800 days does not indicate that the mean solar day is getting longer by a second every 800 days. It will take about 50,000 years for a mean solar day to lengthen by one second (at a rate of 2 ms per century). This rate fluctuates within the range of 1.7–2.3 ms/cy. While the rate due to tidal friction alone is about 2.3 ms/cy, the uplift of Canada and Scandinavia by several metres since the last ice age has temporarily reduced this to 1.7 ms/cy over the last 2,700 years. The correct reason for leap seconds, then, is not the current difference between actual and nominal LOD, but rather the accumulation of this difference over a period of time: Near the end of the 20th century, this difference was about ⁠1/800⁠ of a second per day; therefore, after about 800 days, it accumulated to 1 second (and a leap second was then added).

In the graph of DUT1 above, the excess of LOD above the nominal 86,400 s corresponds to the downward slope of the graph between vertical segments. (The slope became shallower in the 1980s, 2000s and late 2010s to 2020s because of slight accelerations of Earth's rotation temporarily shortening the day.) Vertical position on the graph corresponds to the accumulation of this difference over time, and the vertical segments correspond to leap seconds introduced to match this accumulated difference. Leap seconds are timed to keep DUT1 within the vertical range depicted by the adjacent graph. The frequency of leap seconds therefore corresponds to the slope of the diagonal graph segments, and thus to the excess LOD. Time periods when the slope reverses direction (slopes upwards, not the vertical segments) are times when the excess LOD is negative, that is, when the LOD is below 86,400 s.

## Future

As the Earth's rotation continues to slow, positive leap seconds will be required more frequently. The long-term rate of change of LOD is approximately +1.7 ms per century. At the end of the 21st century, LOD will be roughly 86,400.004 s, requiring a leap second about every 250 days. Over several centuries, the frequency of leap seconds will become problematic. A change in the trend of the UT1 − UTC values was seen beginning around June 2019 in which instead of slowing down (with leap seconds to keep the difference between UT1 and UTC less than 0.9 seconds) the Earth's rotation has sped up, causing this difference to increase. If the trend continues, a negative leap second may be required, which has not been used before.

Some time in the 22nd century, two leap seconds will be required every year. The current practice of only allowing leap seconds in June and December will be insufficient to maintain a difference of less than 1 second, and it might be decided to introduce leap seconds in March and September. In the 25th century, four leap seconds are projected to be required every year, so the current quarterly options would be insufficient.

In April 2001, Rob Seaman of the National Optical Astronomy Observatory proposed that leap seconds be allowed to be added monthly rather than twice yearly.

In 2022 a resolution was adopted by the General Conference on Weights and Measures to redefine UTC and abolish leap seconds, but keep the civil second constant and equal to the SI second, so that sundials would slowly get further and further out of sync with civil time. The leap seconds will be eliminated by 2035. The resolution does not break the connection between UTC and UT1, but increases the maximum allowable difference. The details of what the maximum difference will be and how corrections will be implemented is left for future discussions. This will result in a shift of the sun's movements relative to civil time, with the difference increasing quadratically with time (i.e., proportional to elapsed centuries squared). This is analogous to the shift of seasons relative to the yearly calendar that results from the calendar year not precisely matching the tropical year length. This would be a change in civil timekeeping, and would have a slow effect at first but become drastic over several centuries. UTC (and TAI) would be more and more ahead of UT; it would coincide with local mean time along a meridian drifting eastward faster and faster. Thus, the time system will lose its fixed connection to the geographic coordinates based on the IERS meridian. The difference between UTC and UT would reach 0.5 hours after the year 2600 and 6.5 hours around 4600.

ITU-R Study Group 7 and Working Party 7A were unable to reach consensus on whether to advance the proposal to the 2012 Radiocommunications Assembly; the chairman of Study Group 7 elected to advance the question to the 2012 Radiocommunications Assembly (20 January 2012), but consideration of the proposal was postponed by the ITU until the World Radio Conference in 2015. This conference, in turn, considered the question, but no permanent decision was reached; it only chose to engage in further study with the goal of reconsideration in 2023.

A proposed alternative to the leap second is the leap hour or leap minute, which requires changes only once every few centuries.

The ITU World Radiocommunication Conference 2023 (WRC-23), which was held in Dubai (United Arab Emirates) from 20 November to 15 December 2023, formally recognised Resolution 4 of the 27th CGPM (2022), which decides that the maximum value for the difference (UT1 − UTC) will be increased in or before 2035.

In October 2026 the General Conference on Weights and Measures decided leap seconds would be eliminated beginning 20 May 2027. Since leap seconds usually occur 31 December or 30 June, and it has already been announced there will not be a leap second in December 2026, this effectively means there will be no more leap seconds. See the #Mechanism section for further details.
