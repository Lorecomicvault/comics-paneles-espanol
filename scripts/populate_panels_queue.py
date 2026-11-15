"""
Populate Panels Queue: 30 Paneles Legendarios de Cómics
=======================================================
Genera 30 publicaciones automáticas (3 días completos a 10 posts/día)
con imágenes optimizadas en alta definición y captions hipnóticos.
"""

import json
import os
import shutil
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.image_optimizer import optimize_comic_image

SOURCE_CURATED = Path(r"C:\Users\Vanes\comics en espanol\assets\curated_panels")
QUEUE_DIR = PROJECT_ROOT / "scheduled_queue"

PANELS_CATALOG = [
    {
        "id": "001_wolverine_muerte_adamantium",
        "title": "La Muerte de Wolverine: Convertido en Estatua Eterna",
        "character": "Wolverine",
        "comic_source": "Death of Wolverine #4 (2014)",
        "source_img": "wolverine_muerte_adamantium/scene_04.jpg",
        "hook": "EL FINAL MÁS DOLOROSO DE LOGAN: BAÑADO EN ADAMANTIUM LÍQUIDO 🩸",
        "story": "Sin su factor curativo y con el cuerpo completamente destrozado, Wolverine destruyó los contenedores de Arma X para salvar a sujetos inocentes. El metal hirviendo cayó sobre él, solidificándose en segundos. De rodillas frente al atardecer de Nevada, Logan dio su último aliento en paz, inmortalizado para siempre.",
        "debate_question": "¿Consideras esta la mejor muerte de un superhéroe en la historia del cómic o merecía otro final?",
        "hashtags": "#Wolverine #Logan #MarvelComics #DeathOfWolverine #XMen #ComicsEnEspañol #Marvel #Comics #Geek"
    },
    {
        "id": "002_wonder_woman_bota_batman",
        "title": "Wonder Woman Humilla a Batman bajo su Bota",
        "character": "Wonder Woman & Batman",
        "comic_source": "Wonder Woman: The Hiketeia (2002)",
        "source_img": "wonderwoman_hiketeia_bota_batman/scene_04.jpg",
        "hook": "EL DÍA QUE DIANA APLASTÓ EL ROSTRO DE BATMAN BAJO SU BOTA 👑⚔️",
        "story": "Bajo el sagrado ritual griego de la Hiketeia, Wonder Woman juró con su propia alma proteger a una joven fugitiva. Cuando Batman intentó arrestarla bajo la lluvia de Gotham, Diana no dudó ni un segundo: derribó al Caballero de la Noche y puso su bota pesada sobre su mandíbula con tres palabras demoledoras: 'No. Te. Levantes.'",
        "debate_question": "¿Hizo bien Wonder Woman al priorizar el honor divino sobre la ley de Batman? ¿Quién tiene la razón?",
        "hashtags": "#WonderWoman #Batman #DCComics #TheHiketeia #JusticeLeague #ComicsEnEspañol #DC #ComicsDeCulto"
    },
    {
        "id": "003_magneto_desgarro_adamantium",
        "title": "Magneto Arranca el Adamantium de Wolverine",
        "character": "Magneto vs Wolverine",
        "comic_source": "X-Men Vol. 2 #25 (1993)",
        "source_img": "magneto_fatal_attractions/scene_02.jpg",
        "hook": "¡EL MOMENTO MÁS CRUEL DE MAGNETO CONTRA WOLVERINE! 🧲🩸",
        "story": "Durante la saga Atracciones Fatales en la estación espacial Avalon, Wolverine intentó apuñalar a Magneto. La respuesta del Amo del Magnetismo fue despiadada: manipuló el campo magnético y arrancó el adamantium líquido directamente a través de los poros de la piel de Logan, dejándolo al borde de la muerte.",
        "debate_question": "¿Fue esta la mayor muestra de crueldad de Magneto en los cómics?",
        "hashtags": "#Magneto #Wolverine #XMen #FatalAttractions #MarvelComics #Marvel #ComicsEnEspañol #Mutantes"
    },
    {
        "id": "004_darth_vader_down_rodeado",
        "title": "Darth Vader: Solo Rodeado de Miedo y Hombres Muertos",
        "character": "Darth Vader",
        "comic_source": "Star Wars: Vader Down #1 (2015)",
        "source_img": "darth_vader_down/scene_03.jpg",
        "hook": "VADER RODEADO POR UN EJÉRCITO REBELDE: 'SOLO VEO HOMBRES MUERTOS' ⚔️🌌",
        "story": "Tras derribar su nave en las dunas de Vrogas Vas, cientos de soldados y tanques rebeldes apuntaron sus rifles contra Darth Vader exigiéndole que soltara sus armas porque estaba rodeado. La respuesta del Lord Sith heló la sangre de la galaxia: 'Lo único que me rodea es el miedo... y hombres muertos'. Segundos después, encendió su sable carmesí.",
        "debate_question": "¿Es esta la frase y viñeta más intimidante de todo Star Wars?",
        "hashtags": "#DarthVader #StarWars #VaderDown #Sith #ComicsEnEspañol #Lucasfilm #StarWarsComics #LordVader"
    },
    {
        "id": "005_joker_rostro_engrapado",
        "title": "El Rostro Engrapado del Joker",
        "character": "Joker",
        "comic_source": "Batman: Death of the Family (2012)",
        "source_img": "06_joker_mascara_cara_rebanada_death_of_family/scene_02.jpg",
        "hook": "LA PESADILLA MÁS PERTURBADORA DEL JOKER EN GOTHAM 🃏💀",
        "story": "El Joker permitió voluntariamente que el villano Dollmaker le rebanara la piel del rostro para dejarla pudriéndose en una celda de Arkham. Un año después regresó a reclamarla, sujetando la carne descompuesta a su cráneo con alambres, garfios y grapas quirúrgicas. Scott Snyder y Greg Capullo crearon la versión más terrorífica del Príncipe Payaso.",
        "debate_question": "¿Cuál es tu diseño favorito del Joker en los cómics? ¿Prefieres este estilo macabro o el clásico?",
        "hashtags": "#Joker #Batman #DeathOfTheFamily #DCComics #ScottSnyder #GothamCity #ComicsEnEspañol #TerrorComics"
    },
    {
        "id": "006_superman_vs_the_elite",
        "title": "Superman: Ojos en Llamas y Juicio a The Elite",
        "character": "Superman",
        "comic_source": "Action Comics #775 (2001)",
        "source_img": "superman_vs_the_elite/scene_03.jpg",
        "hook": "SUPERMAN ENFURECIDO: CUANDO EL HOMBRE DE ACERO PIERDE LA PACIENCIA 🦸‍♂️🔥",
        "story": "The Elite creía que el código moral de Superman era débil y obsoleto. Para demostrarles por qué nunca cruza la línea, Superman fingió volverse un tirano sin piedad: desmanteló a cada miembro con frialdad aterradora y neutralizó la mente de Manchester Black con visión de calor microscópica. Una obra maestra sobre el verdadero heroísmo.",
        "debate_question": "¿Debe un superhéroe matar a los peores villanos o mantener la moral intacta como Superman?",
        "hashtags": "#Superman #TheElite #ActionComics #DCComics #HombreDeAcero #ComicsEnEspañol #DC #Superheroes"
    },
    {
        "id": "007_nova_annihilus_desgarro",
        "title": "Nova Prime Desgarra a Annihilus por la Garganta",
        "character": "Nova Prime",
        "comic_source": "Annihilation #6 (2007)",
        "source_img": "nova_annihilus_desgarro/scene_04.jpg",
        "hook": "¡EL DESGARRO MÁS SALVAJE EN LA HISTORIA CÓSMICA DE MARVEL! 💫💥",
        "story": "Con galaxias enteras aniquiladas y el cuerpo Nova Corps destruido, Richard Rider cargó la Fuerza Nova completa en sus venas. En el clímax de Annihilation, Nova clavó su puño en la boca del conquistador cósmico Annihilus y tiró con todas sus fuerzas, volteando sus órganos de adentro hacia afuera con el grito: '¡Esto es por los Nova Corps!'.",
        "debate_question": "¿Es Annihilation el mejor evento cósmico que ha publicado Marvel en su historia?",
        "hashtags": "#Nova #Annihilus #Annihilation #MarvelComics #MarvelCosmic #RichardRider #ComicsEnEspañol #Marvel"
    },
    {
        "id": "008_marvel_zombies_devoran_galactus",
        "title": "Los Vengadores Zombis Devoran a Galactus",
        "character": "Marvel Zombies",
        "comic_source": "Marvel Zombies #5 (2006)",
        "source_img": "zombies_consumen_galactus_poder_infinito/scene_03.jpg",
        "hook": "CUANDO LOS VENGADORES INFECTADOS SE COMIERON VIVO A GALACTUS 🧟‍♂️🌌",
        "story": "El virus del hambre no respetó ni al devorador de mundos. Tras derribar a Galactus con un cañón cósmico improvisado, Spider-Man, Iron Man, Wolverine, Giant-Man y Hulk se abalanzaron sobre el titán y devoraron su carne divina. Al consumirlo, absorbieron el Poder Cósmico y viajaron por el universo devorando planetas enteros.",
        "debate_question": "¿Qué héroe zombificado te dio más miedo en la serie de Marvel Zombies?",
        "hashtags": "#MarvelZombies #Galactus #SpiderMan #Hulk #MarvelComics #Zombies #ComicsEnEspañol #MarvelMultiverse"
    },
    {
        "id": "009_captain_america_asesinato_civil_war",
        "title": "El Asesinato del Capitán América en las Escaleras del Juzgado",
        "character": "Captain America",
        "comic_source": "Captain America Vol. 5 #25 (2007)",
        "source_img": "captain_america_asesinato_civil_war/scene_03.jpg",
        "hook": "EL DÍA QUE EL CAPITÁN AMÉRICA FUE ASESINADO ANTE LOS OJOS DEL MUNDO 🇺🇸🩸",
        "story": "Tras entregarse para frenar la Guerra Civil, Steve Rogers subía esposado las escalinatas del palacio de justicia en Nueva York. Un disparo de francotirador de Crossbones y tres tiros a quemarropa de Sharon Carter (manipulada mentalmente por el Dr. Faustus) sellaron el destino del mayor símbolo de la libertad. Una viñeta que paralizó las noticias reales en 2007.",
        "debate_question": "¿Team Cap o Team Iron Man? ¿Quién tenía la razón en el conflicto de Civil War?",
        "hashtags": "#CaptainAmerica #CivilWar #SteveRogers #MarvelComics #EdBrubaker #ComicsEnEspañol #Marvel #Avengers"
    },
    {
        "id": "010_morlun_pesadilla_ojos",
        "title": "Morlun: Ojos en las Palmas de las Manos",
        "character": "Spider-Man & Morlun",
        "comic_source": "The Amazing Spider-Man #35 (2001)",
        "source_img": "morlun_devora_ojo_spiderman/scene_04.jpg",
        "hook": "LA MALDICIÓN TOTÉMICA DE MORLUN: OJOS BROTANDO DE SUS MANOS 🕷️👁️",
        "story": "J. Michael Straczynski y John Romita Jr. revolucionaron la mitología de Spider-Man al introducir a Morlun, un vampiro milenario que caza avatares arácnidos para alimentarse de su esencia vital. Cuando la energía totémica despierta, ojos rojos demoníacos brotan de las palmas de sus manos, revelando su naturaleza depredadora.",
        "debate_question": "¿Es Morlun el villano más aterrador al que se ha enfrentado Spider-Man?",
        "hashtags": "#SpiderMan #Morlun #MarvelComics #SpiderVerse #AmazingSpiderMan #ComicsEnEspañol #PeterParker"
    },
    {
        "id": "011_doctor_doom_desgarra_thanos",
        "title": "God Emperor Doom Arranca la Espina Dorsal de Thanos",
        "character": "Doctor Doom vs Thanos",
        "comic_source": "Secret Wars #8 (2015)",
        "source_img": "59_doctor_doom_destruye_thanos_secret_wars/scene_04.jpg",
        "hook": "DOCTOR DOOM MATANDO A THANOS DE UN SOLO GOLPE: '¿TIENES UN GUANTELETE?' 👑💀",
        "story": "Durante Secret Wars en Battleworld, Thanos desafió al Dios Emperador Doom creyendo que su poder infinito no era nada. Doom simplemente se acercó, le preguntó si aún poseía el Guantelete del Infinito y, al escuchar la negativa del Titán Loco, le arrancó el esqueleto y la columna vertebral con una sola mano, reduciéndolo a cenizas.",
        "debate_question": "¿Es el Doctor Doom el mejor villano de toda la historia de Marvel? Argumenta tu respuesta 👇",
        "hashtags": "#DoctorDoom #Thanos #SecretWars #MarvelComics #Doom #Marvel #ComicsEnEspañol #JonathanHickman"
    },
    {
        "id": "012_sentry_descuartiza_ares",
        "title": "Sentry Descuartiza a Ares en Siege",
        "character": "Sentry vs Ares",
        "comic_source": "Siege #2 (2010)",
        "source_img": "54_sentry_descuartiza_ares_siege/scene_04.jpg",
        "hook": "¡LA MUERTE MÁS VISCERAL DE ASGARD! SENTRY PARTE EN DOS AL DIOS DE LA GUERRA ⚡🩸",
        "story": "Durante el asedio de Norman Osborn contra Asgard, Ares descubrió que había sido engañado y juró decapitar a Osborn. Antes de tocarlo, Robert Reynolds (Sentry) atrapó al Dios olímpico de la guerra en el aire y, con una fuerza brutal y aterradora, lo partió por la mitad de arriba hacia abajo frente a ambos ejércitos atónitos.",
        "debate_question": "¿Es Sentry demasiado poderoso para el universo Marvel? ¿Debería tener límites?",
        "hashtags": "#Sentry #Ares #Siege #MarvelComics #Asgard #ComicsEnEspañol #Marvel #DarkAvengers"
    },
    {
        "id": "013_bane_quiebra_espalda_batman",
        "title": "Bane Quiebra la Espalda de Batman en Knightfall",
        "character": "Bane vs Batman",
        "comic_source": "Batman #497 (1993)",
        "source_img": "26_batman_quiebra_espalda_bane_arkham/scene_04.jpg",
        "hook": "EL CRUJIDO QUE ROMPIÓ A GOTHAM: BANE PARTE A BATMAN EN DOS 🦇💥",
        "story": "Tras agotar a Batman liberando a todos los internos de Arkham, Bane esperó en la propia Mansión Wayne. Con el Murciélago deshidratado y sin fuerzas, Bane lo levantó sobre su cabeza y lo azotó contra su rodilla, quebrando su columna vertebral en el panel más icónico de los años noventa.",
        "debate_question": "¿Cuál ha sido la derrota más dolorosa de Batman en los cómics?",
        "hashtags": "#Batman #Bane #Knightfall #DCComics #Gotham #ComicsEnEspañol #DC #BatmanComics"
    },
    {
        "id": "014_injustice_alfred_superman",
        "title": "Alfred Humilla a Superman con una Pastilla de Kriptonita",
        "character": "Alfred Pennyworth vs Superman",
        "comic_source": "Injustice: Gods Among Us #36 (2013)",
        "source_img": "57_injustice_alfred_superman/scene_04.jpg",
        "hook": "¡EL CABEZAZO DE ALFRED QUE FRACTURÓ LA NARIZ DE SUPERMAN! 🥊🦸‍♂️",
        "story": "Superman invadió la Batcueva y quebró la espalda de Bruce Wayne frente a Alfred. Lo que Clark Kent no sabía es que el mayordomo más leal del mundo acababa de consumir una nanópildora de fuerza sobrehumana. Alfred le propinó un cabezazo devastador que le destrozó la nariz al tirano kryptoniano diciendo: 'Estoy profundamente decepcionado de usted'.",
        "debate_question": "¿Es Alfred el personaje con más agallas de todo el universo de Batman?",
        "hashtags": "#Alfred #Superman #Injustice #Batman #DCComics #ComicsEnEspañol #InjusticeGodsAmongUs"
    },
    {
        "id": "015_world_war_hulk_black_bolt",
        "title": "World War Hulk Aplasta a Black Bolt en la Luna",
        "character": "Hulk vs Black Bolt",
        "comic_source": "World War Hulk #1 (2007)",
        "source_img": "62_hulk_world_war_venganza_illuminati/scene_04.jpg",
        "hook": "HULK ENFURECIDO VS EL REY DE LOS INHUMANOS EN LA LUNA 🌕💥",
        "story": "Exiliado al espacio por los Illuminati y tras la muerte de su reina Caiera en Sakaar, el Gigante Esmeralda regresó a la Tierra por pura venganza. Su primera parada fue la Luna, donde enfrentó a Black Bolt. Ni siquiera el susurro destructor del monarca inhumano pudo frenar la furia de Hulk, quien lo derribó bañado en sangre.",
        "debate_question": "¿Consideras World War Hulk la versión más poderosa de Hulk de todos los tiempos?",
        "hashtags": "#Hulk #WorldWarHulk #BlackBolt #MarvelComics #Inhumans #ComicsEnEspañol #Marvel #Smash"
    },
    {
        "id": "016_batman_who_laughs_dark_multiverse",
        "title": "El Origen del Batman que Ríe",
        "character": "The Batman Who Laughs",
        "comic_source": "Dark Days: The Batman Who Laughs #1 (2017)",
        "source_img": "55_batman_que_rie_dark_multiverse/scene_04.jpg",
        "hook": "¿QUÉ PASA SI BATMAN MATA AL JOKER Y SE CONTAGIA CON SU TOXINA? 🦇🃏",
        "story": "En el Multiverso Oscuro, Batman finalmente rompió el cuello del Joker. Pero el corazón del payaso liberó una toxina purificada que infectó el lóbulo frontal de Bruce. Con la mente táctica de Batman y la locura sádica del Joker, aniquiló a toda la Liga de la Justicia y a sus propios aliados en cuestión de horas.",
        "debate_question": "¿Fue el Batman que Ríe el villano más aterrador de la era moderna de DC?",
        "hashtags": "#TheBatmanWhoLaughs #Batman #DCComics #DarkNightsMetal #Joker #ComicsEnEspañol #DC"
    },
    {
        "id": "017_venom_dios_de_la_luz_knull",
        "title": "Venom se Convierte en el Dios de la Luz",
        "character": "Venom",
        "comic_source": "King in Black #5 (2021)",
        "source_img": "65_venom_dios_de_la_luz_knull/scene_04.jpg",
        "hook": "¡VENOM SE TRANSFORMA EN EL DIOS DE LA LUZ Y DESTRUYE A KNULL! 🌌⚔️",
        "story": "En la conclusión de King in Black por Donny Cates y Ryan Stegman, Eddie Brock fue elegido por la Fuerza Enigma primordial. Fusionando el hacha de Thor y la tabla de Silver Surfer en una espada colosal, Venom se convirtió en el Dios de la Luz, destrozó al Dios del Abismo Knull y arrojó sus restos al corazón del Sol.",
        "debate_question": "¿Te gustó ver a Venom ascender a deidad cósmica o prefieres al clásico antihéroe urbano?",
        "hashtags": "#Venom #KingInBlack #Knull #EddieBrock #MarvelComics #DonnyCates #ComicsEnEspañol #Marvel"
    },
    {
        "id": "018_old_man_logan_estomago_hulk",
        "title": "Old Man Logan Desgarra el Vientre de Hulk",
        "character": "Old Man Logan vs Maestro Hulk",
        "comic_source": "Wolverine: Old Man Logan #73 (2009)",
        "source_img": "old_man_logan_estomago_hulk/scene_04.jpg",
        "hook": "HULK SE TRAGÓ VIVO A LOGAN... Y FUE EL PEOR ERROR DE SU VIDA 🩸🐺",
        "story": "En el páramo distópico de Mark Millar y Steve McNiven, la despiadada familia Hulk masacró a la familia de Logan. Un Bruce Banner anciano y degenerado devoró entero a Wolverine. Pero el factor curativo de Logan se reactivó en el estómago, sacó sus garras de adamantium y desgarró el vientre de Hulk desde adentro hacia afuera.",
        "debate_question": "¿Es Old Man Logan la mejor historia alternativa de Marvel jamás escrita?",
        "hashtags": "#OldManLogan #Wolverine #Hulk #MarkMillar #MarvelComics #ComicsEnEspañol #Marvel #MarvelComics"
    },
    {
        "id": "019_doomsday_humilla_darkseid",
        "title": "Doomsday Masacra a Darkseid en Apokolips",
        "character": "Doomsday vs Darkseid",
        "comic_source": "Superman/Doomsday: Hunter/Prey #1 (1994)",
        "source_img": "doomsday_humilla_darkseid_apokolips/scene_04.jpg",
        "hook": "¡DOOMSDAY RESISTIÓ EL EFECTO OMEGA Y HUMILLÓ A DARKSEID! 💀🔥",
        "story": "Cuando el monstruo que mató a Superman aterrizó en Apokolips, el tirano cósmico Darkseid disparó sus míticos Rayos Omega, creyendo que borraría a la bestia de la existencia. Doomsday no solo resistió el ataque intacto, sino que propinó a Darkseid la paliza más humillante de su vida en su propio trono.",
        "debate_question": "¿Existe algún ser en DC capaz de vencer a Doomsday sin enviarlo al fin de los tiempos?",
        "hashtags": "#Doomsday #Darkseid #Superman #DCComics #Apokolips #ComicsEnEspañol #DC #Villanos"
    },
    {
        "id": "020_invincible_conquest_sangre",
        "title": "Invincible vs Conquest: La Batalla más Sangrienta",
        "character": "Invincible vs Conquest",
        "comic_source": "Invincible #64 (2009)",
        "source_img": "invincible_conquest_asalto_brutal_sangre/scene_04.jpg",
        "hook": "¡EL CABEZAZO QUE DESTROZÓ EL CRÁNEO DE CONQUEST EN INVINCIBLE! 🩸🦸‍♂️",
        "story": "El viltrumita más sanguinario del Imperio, Conquest, llegó a la Tierra para forzar a Mark Grayson a someter el planeta. Tras casi asesinar a Atom Eve, Mark enloqueció de dolor y furia: con ambos brazos y piernas fracturados, usó su propia frente para golpear el rostro de Conquest una y otra vez hasta pulverizar sus huesos.",
        "debate_question": "¿Es esta la pelea más visceral e intensa de todo el cómic independiente moderno?",
        "hashtags": "#Invincible #Conquest #RobertKirkman #ImageComics #OmniMan #ComicsEnEspañol #Comics"
    },
    {
        "id": "021_cyclops_disparo_optico_centinela",
        "title": "Cyclops Sin Visor Pulveriza a un Centinela",
        "character": "Cyclops",
        "comic_source": "Astonishing X-Men #8 (2005)",
        "source_img": "21_cyclops_disparo_optico_centinela/scene_04.jpg",
        "hook": "CUANDO CYCLOPS SE QUITÓ EL VISOR: 'FUERA DE MI CÉSPED' 💥🔴",
        "story": "Escrito por Joss Whedon y dibujado por John Cassaday. Cuando un Centinela gigante atacó la Mansión X, Scott Summers no dudó: ordenó a todos que se apartaran, se retiró el visor de cuarzo de rubí y desató la potencia total acumulada de su dimensión óptica, borrando el bosque y al robot colosal en una fracción de segundo.",
        "debate_question": "¿Está Cyclops infravalorado respecto a otros líderes de Marvel?",
        "hashtags": "#Cyclops #XMen #AstonishingXMen #MarvelComics #ScottSummers #ComicsEnEspañol #Mutantes"
    },
    {
        "id": "022_punisher_esclavistas_incinerador",
        "title": "Frank Castle Castiga a los Esclavistas en el Incinerador",
        "character": "The Punisher",
        "comic_source": "The Punisher MAX: The Slavers #30 (2006)",
        "source_img": "23_punisher_esclavistas_incinerador/scene_04.jpg",
        "hook": "LA JUSTICIA MÁS CRUDA DE THE PUNISHER EN LA ERA MAX 💀🔥",
        "story": "Garth Ennis escribió la historia más brutal y oscura de Frank Castle al enfrentar a una red de traficantes y proxenetas en Nueva York. Al capturar a Cristu Bulat, Castle no gastó una sola bala: lo obligó a confesar frente a la puerta del horno incinerador y lo introdujo lentamente. Un momento de furia pura e implacable.",
        "debate_question": "¿Es la etapa MAX de Garth Ennis la versión definitiva de The Punisher?",
        "hashtags": "#ThePunisher #FrankCastle #MarvelMAX #GarthEnnis #MarvelComics #ComicsEnEspañol #Antiheroes"
    },
    {
        "id": "023_spiderman_arranca_mandibula_escorpion",
        "title": "Superior Spider-Man Arranca la Mandíbula de Escorpión",
        "character": "Superior Spider-Man",
        "comic_source": "Amazing Spider-Man #700 (2012)",
        "source_img": "51_spiderman_escorpion_mandibula_superior/scene_04.jpg",
        "hook": "EL GOLPE QUE DEMOSTRÓ LA VERDADERA FUERZA OCULTA DE SPIDER-MAN 🕷️💥",
        "story": "Cuando Otto Octavius tomó el cuerpo de Peter Parker, no entendía por qué Peter solía tener tantos problemas con sus villanos. En su primera pelea contra Escorpión, conectó un puñetazo directo a la mandíbula con fuerza total... arrancándole el hueso facial de cuajo. Otto comprendió aterrado que Peter siempre se contuvo para no matar a nadie.",
        "debate_question": "¿Qué villano de Spider-Man hubiera muerto si Peter no se contuviera en cada golpe?",
        "hashtags": "#SuperiorSpiderMan #SpiderMan #DocOck #MarvelComics #Scorpion #DanSlott #ComicsEnEspañol"
    },
    {
        "id": "024_spiderman_back_in_black_kingpin",
        "title": "Spider-Man Humilla a Kingpin en Prisión",
        "character": "Spider-Man vs Kingpin",
        "comic_source": "The Amazing Spider-Man #542 (2007)",
        "source_img": "53_spiderman_back_in_black_kingpin/scene_04.jpg",
        "hook": "SPIDER-MAN DE NEGRO DESTRUYE A KINGPIN: 'NO VINE A MATARTE HOY' 🕷️🖤",
        "story": "Tras el disparo que dejó a la Tía May al borde de la muerte, Peter Parker se colocó el traje negro y fue directamente a la prisión de Ryker's Island. Sin chistes ni bromas, desnudó a Kingpin frente a todos los reclusos y le dio una paliza descomunal, amenazando con llenar sus pulmones de telaraña si su tía no sobrevivía.",
        "debate_question": "¿Es Spider-Man con traje negro el personaje más intimidante de Marvel?",
        "hashtags": "#SpiderMan #Kingpin #BackInBlack #MarvelComics #PeterParker #WilsonFisk #ComicsEnEspañol"
    },
    {
        "id": "025_drax_arranca_corazon_thanos",
        "title": "Drax el Destructor Arranca el Corazón de Thanos",
        "character": "Drax vs Thanos",
        "comic_source": "Annihilation #4 (2006)",
        "source_img": "45_annihilation_drax_thanos_corazon/scene_04.jpg",
        "hook": "¡EL DÍA QUE DRAX CUMPLIÓ SU PROPÓSITO Y MATÓ A THANOS! 🗡️💀",
        "story": "Creado por la entidad cósmica Kronos con el único fin biológico de erradicar al Titán Loco, Drax atravesó hordas insectoides para alcanzar a Thanos. Justo cuando Thanos intentaba desactivar el cañón de Galactus para salvar el cosmos, Drax apareció por la espalda y perforó su pecho con su puño, arrancándole el corazón palpitante.",
        "debate_question": "¿Fue un error que Drax matara a Thanos en ese instante crítico para el universo?",
        "hashtags": "#Drax #Thanos #Annihilation #MarvelComics #CosmicMarvel #ComicsEnEspañol #Marvel"
    },
    {
        "id": "026_bullseye_mata_karen_page",
        "title": "Bullseye Asesina a Karen Page en la Iglesia",
        "character": "Daredevil & Bullseye",
        "comic_source": "Daredevil Vol. 2 #5 (1999)",
        "source_img": "46_daredevil_muerte_karen_page/scene_04.jpg",
        "hook": "LA MAYOR TRAGEDIA DE DAREDEVIL: EL CLUB QUE ATRAVESÓ A KAREN PAGE 🦯💔",
        "story": "En la aclamada saga Guardian Devil de Kevin Smith y Joe Quesada, Bullseye irrumpió en la iglesia donde Matt Murdock protegía a un bebé inocente. Con puntería letal, arrojó el propio bastón de Daredevil hacia Matt; pero Karen Page se interpuso en la trayectoria, recibiendo el impacto mortal en el pecho para salvar al amor de su vida.",
        "debate_question": "¿Es Bullseye el enemigo más sádico y personal de Daredevil?",
        "hashtags": "#Daredevil #Bullseye #KarenPage #KevinSmith #MarvelComics #ComicsEnEspañol #MattMurdock"
    },
    {
        "id": "027_flashpoint_carta_thomas_wayne",
        "title": "La Carta de Thomas Wayne a Bruce en Flashpoint",
        "character": "Batman (Bruce & Thomas Wayne)",
        "comic_source": "Flashpoint #5 (2011)",
        "source_img": "43_flashpoint_carta_thomas_wayne/scene_04.jpg",
        "hook": "EL MOMENTO DONDE BATMAN LLORÓ: LA CARTA DE SU PADRE ✉️🦇",
        "story": "Tras restablecer la línea temporal destrozada de Flashpoint, Barry Allen visitó la Batcueva para entregarle a Bruce un último regalo del universo alternativo: una carta escrita a mano por Thomas Wayne antes de morir. Las lágrimas rodaron por la máscara de Batman al leer: 'Sé fuerte. Sé el hombre que debías ser. Sé mi hijo'.",
        "debate_question": "¿Consideras esta la escena más conmovedora en toda la historia de Batman?",
        "hashtags": "#Batman #Flashpoint #ThomasWayne #Flash #DCComics #GeoffJohns #ComicsEnEspañol #DC"
    },
    {
        "id": "028_flash_rompe_cuello_reverse_flash",
        "title": "Barry Allen Rompe el Cuello de Reverse-Flash",
        "character": "Flash vs Reverse-Flash",
        "comic_source": "The Flash #324 (1983)",
        "source_img": "36_flash_barry_allen_rompe_cuello_reverse_flash/scene_04.jpg",
        "hook": "CUANDO FLASH MATÓ A REVERSE-FLASH PARA SALVAR A SU PROMETIDA ⚡💀",
        "story": "Eobard Thawne ya había asesinado a Iris West en el pasado. Cuando Thawne corrió a la iglesia para asesinar también a Fiona Webb (la nueva prometida de Barry), Flash lo interceptó a la velocidad de la luz. En un desesperado intento por frenarlo, Barry lo tomó del cuello y, con el impulso de la carrera, quebró su nuca, enfrentando un juicio histórico por homicidio.",
        "debate_question": "¿Estuvo justificado que Barry Allen matara a Thawne para salvar una vida?",
        "hashtags": "#Flash #ReverseFlash #BarryAllen #EobardThawne #DCComics #ComicsEnEspañol #DC"
    },
    {
        "id": "029_iron_man_demonio_en_la_botella",
        "title": "Tony Stark Frente al Espejo: Demonio en la Botella",
        "character": "Iron Man",
        "comic_source": "The Invincible Iron Man #128 (1979)",
        "source_img": "29_iron_man_demonio_botella_espejo/scene_04.jpg",
        "hook": "LA PEOR BATALLA DE TONY STARK NO FUE CONTRA UN VILLANO, SINO CONTRA SÍ MISMO 🍸💔",
        "story": "David Michelinie y Bob Layton crearon un antes y un después en los cómics con 'Demon in a Bottle'. Lejos de monstruos alienígenas, Tony Stark tocó fondo sumido en el alcoholismo tras perder su empresa y el control de su armadura. La viñeta de Tony demacrado, con el cabello despeinado frente al espejo sosteniendo una botella, es historia viva del noveno arte.",
        "debate_question": "¿Es Demonio en la Botella la historia más humana y realista de Marvel?",
        "hashtags": "#IronMan #TonyStark #DemonInABottle #MarvelComics #Avengers #ComicsEnEspañol #Marvel"
    },
    {
        "id": "030_hulk_dos_mitades_ultimate_wolverine",
        "title": "Hulk Parte a Wolverine en Dos Mitades",
        "character": "Hulk vs Ultimate Wolverine",
        "comic_source": "Ultimate Wolverine vs. Hulk #1 (2006)",
        "source_img": "82_ultimate_wolverine_vs_hulk_dos_mitades/scene_04.jpg",
        "hook": "¡HULK DESGARRÓ A WOLVERINE EN DOS Y LANZÓ SUS PIERNAS A LA MONTAÑA! 🩸🐺",
        "story": "Damon Lindelof y Leinil Francis Yu abrieron esta salvaje miniserie en las montañas nevadas del Tíbet con una escena imborrable: Wolverine despierta arrastrándose con sus manos sobre la nieve, solo para darse cuenta de que Hulk le arrancó la mitad inferior del cuerpo y arrojó sus piernas a la cima de otra montaña a cuatro millas de distancia.",
        "debate_question": "¿Quién ganaría en un combate a muerte definitivo: Hulk o Wolverine?",
        "hashtags": "#Hulk #Wolverine #UltimateMarvel #MarvelComics #ComicsEnEspañol #Marvel #Mutantes"
    }
]


def populate_queue():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    created_count = 0

    print("===========================================================")
    print(f"📦 POBLANDO COLA DE PANELES CON {len(PANELS_CATALOG)} MOMENTOS ÉPICOS")
    print(f"   Destino: {QUEUE_DIR}")
    print("===========================================================")

    for idx, item in enumerate(PANELS_CATALOG, 1):
        slot_name = item["id"]
        target_dir = QUEUE_DIR / slot_name
        target_dir.mkdir(parents=True, exist_ok=True)

        img_target = target_dir / "image.jpg"
        meta_target = target_dir / "metadata.json"

        # Check source image
        src_rel = item["source_img"]
        src_path = SOURCE_CURATED / src_rel

        if not src_path.exists():
            print(f"⚠️ Imagen fuente no encontrada para {slot_name}: {src_path}")
            continue

        # Optimize image with cinematic color grading for Facebook
        try:
            optimize_comic_image(src_path, img_target, for_instagram=False)
        except Exception as e:
            print(f"Error optimizando {src_path}: {e}. Copiando directo...")
            shutil.copy2(src_path, img_target)

        # Write metadata
        metadata = {
            "slot": idx,
            "id": item["id"],
            "title": item["title"],
            "character": item["character"],
            "comic_source": item["comic_source"],
            "hook": item["hook"],
            "story": item["story"],
            "debate_question": item["debate_question"],
            "hashtags": item["hashtags"],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(meta_target, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        created_count += 1
        print(f"✅ [{idx:02d}/{len(PANELS_CATALOG)}] Encolado: {slot_name} ({item['title']})")

    print("\n===========================================================")
    print(f"🎉 COLA POBLADA CON ÉXITO: {created_count} PANELES LISTOS")
    print("===========================================================")


if __name__ == "__main__":
    populate_queue()
