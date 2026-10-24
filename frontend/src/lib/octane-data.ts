export type Reg = "UN R48" | "UN R148" | "UN R150" | "UN R10";
export type Category =
  | "Photometric"
  | "Installation & Visibility"
  | "Markings"
  | "Electrical/EMC"
  | "Environmental"
  | "COP";

export interface Obligation {
  id: string;
  reg: Reg;
  para: string;
  page: number;
  category: Category;
  tag: string;
  text: string;
  test: string;
}

export const REGS: Reg[] = ["UN R48", "UN R148", "UN R150", "UN R10"];
export const CATEGORIES: Category[] = [
  "Photometric",
  "Installation & Visibility",
  "Markings",
  "Electrical/EMC",
  "Environmental",
  "COP",
];

export const REG_TITLES: Record<Reg, string> = {
  "UN R48": "Installation of lighting and light-signalling devices",
  "UN R148": "Light-signalling devices (LSD)",
  "UN R150": "Retro-reflective devices and markings",
  "UN R10": "Electromagnetic compatibility",
};

export const REG_SLUG: Record<Reg, string> = {
  "UN R48": "R48",
  "UN R148": "R148",
  "UN R150": "R150",
  "UN R10": "R10",
};

const rearLamp: Obligation[] = [
  {
    "id": "R-0001",
    "reg": "UN R48",
    "para": "5.1",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The lighting and light-signalling devices shall be so fitted that under normal conditions of use as defined in paragraphs 2.3.10., 2.3.10.1. and 2.3.10.2. and notwithstanding any vibrations to which they may be subjected, they retain the characteristics prescribed by this Regulation.",
    "test": "Inspect the rear lamp mounting and verify after vibration exposure in normal use that photometric, colour and position characteristics are unchanged."
  },
  {
    "id": "R-0002",
    "reg": "UN R48",
    "para": "5.1",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The lighting and light-signalling devices shall be so fitted that under normal conditions of use and notwithstanding any vibrations to which they may be subjected, they enable the vehicle to comply with the requirements of this Regulation.",
    "test": "Verify on the installed vehicle that all R48 installation requirements for the rear lamp functions are met in normal condition of use."
  },
  {
    "id": "R-0003",
    "reg": "UN R48",
    "para": "5.1",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In particular, it shall not be possible for the lamps to be inadvertently maladjusted.",
    "test": "Check that the rear lamp fixings (clips, screws, locating pins) prevent unintended displacement or misalignment."
  },
  {
    "id": "R-0004",
    "reg": "UN R48",
    "para": "5.3",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "For all light-signalling devices, the reference axis of the lamp when fitted to the vehicle shall be parallel to the bearing plane of the vehicle on the road.",
    "test": "Measure the installed reference axis of each rear lamp function against the ground plane."
  },
  {
    "id": "R-0005",
    "reg": "UN R48",
    "para": "5.3",
    "page": 19,
    "category": "Markings",
    "tag": "Retro-reflection",
    "text": "The reference axis of the lamp when fitted to the vehicle shall be parallel to the median longitudinal plane of the vehicle in the case of all other signalling devices (other than side retro-reflectors and side-marker lamps).",
    "test": "Measure the installed reference axis of the rear position, stop and reversing lamps and rear retro-reflector relative to the vehicle median longitudinal plane."
  },
  {
    "id": "R-0006",
    "reg": "UN R48",
    "para": "5.3",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In each direction a tolerance of \u00b13\u00b0 shall be allowed for the orientation of the reference axis.",
    "test": "Confirm that measured deviations of the reference axis do not exceed \u00b13\u00b0 horizontally and vertically."
  },
  {
    "id": "R-0007",
    "reg": "UN R48",
    "para": "5.3",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Any specific instructions as regards fitting laid down by the manufacturer shall be complied with.",
    "test": "Compare the installation against the lamp manufacturer's fitting instructions."
  },
  {
    "id": "R-0008",
    "reg": "UN R48",
    "para": "5.4",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In the absence of specific instructions, the height and orientation of the lamps shall be verified with the vehicle unladen and placed on a flat, horizontal surface, in the condition defined in paragraphs 2.3.10., 2.3.10.1. and 2.3.10.2.",
    "test": "Perform height and orientation measurements on the unladen vehicle on a flat horizontal surface in normal condition of use."
  },
  {
    "id": "R-0009",
    "reg": "UN R48",
    "para": "5.5.1",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In the absence of specific instructions lamps constituting a pair shall be fitted to the vehicle symmetrically in relation to the median longitudinal plane (this estimate to be based on the exterior geometrical form of the lamp and not on the edge of its illuminating surface).",
    "test": "Measure left and right rear lamp positions relative to the median longitudinal plane and verify symmetry of exterior form."
  },
  {
    "id": "R-0010",
    "reg": "UN R48",
    "para": "5.5.2",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In the absence of specific instructions lamps constituting a pair shall be symmetrical to one another in relation to the median longitudinal plane; this requirement is not valid with regard to the interior structure of the lamp.",
    "test": "Compare the exterior geometry of the left and right rear lamps for mirror symmetry."
  },
  {
    "id": "R-0011",
    "reg": "UN R48",
    "para": "5.5.3",
    "page": 19,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "In the absence of specific instructions lamps constituting a pair shall satisfy the same colorimetric requirements.",
    "test": "Check colour approval/measurement of left and right lamps of each function for identical colour category."
  },
  {
    "id": "R-0012",
    "reg": "UN R48",
    "para": "5.5.4",
    "page": 19,
    "category": "Photometric",
    "tag": "Photometric Provision",
    "text": "In the absence of specific instructions lamps constituting a pair shall have substantially identical photometric characteristics; this shall not apply to a matched pair of a function.",
    "test": "Compare photometric approval data of left and right rear lamps of each function."
  },
  {
    "id": "R-0013",
    "reg": "UN R48",
    "para": "5.5.5",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Lateral Position",
    "text": "In case of lamps incorporating a manufacturer logo, only two lateral logos (one on each side) or one central logo can be fitted on the rear of the vehicle.",
    "test": "Count logos incorporated in rear lamps and verify maximum two lateral or one central."
  },
  {
    "id": "R-0014",
    "reg": "UN R48",
    "para": "5.5.5",
    "page": 19,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "All logos that are not vehicle manufacturer or body manufacturer logos are prohibited.",
    "test": "Verify any logo in the rear lamp is a vehicle or body manufacturer logo."
  },
  {
    "id": "R-0015",
    "reg": "UN R48",
    "para": "5.7.1",
    "page": 19,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "Lamps may be grouped, combined or reciprocally incorporated with one another provided that all requirements regarding colour, position, orientation, geometric visibility, electrical connections and other requirements, if any, are fulfilled.",
    "test": "Verify each function in the grouped rear lamp individually meets colour, position, orientation, visibility and electrical requirements."
  },
  {
    "id": "R-0016",
    "reg": "UN R48",
    "para": "5.7.1.1",
    "page": 20,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The photometric and colorimetric requirements of a lamp shall be fulfilled when all other functions with which this lamp is grouped, combined or reciprocally incorporated are switched OFF.",
    "test": "Check approval photometry and colour of each function measured with the other rear lamp functions OFF."
  },
  {
    "id": "R-0017",
    "reg": "UN R48",
    "para": "5.7.1.1",
    "page": 20,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "When a rear position lamp is reciprocally incorporated with one or more other function(s) which can be switched ON together with them, the requirements regarding colour of each of these other functions shall be fulfilled when the reciprocally incorporated function(s) and the rear position lamps are switched ON.",
    "test": "With rear position lamp and reciprocally incorporated function (e.g. stop lamp) both ON, verify colour of the other function."
  },
  {
    "id": "R-0018",
    "reg": "UN R48",
    "para": "5.8",
    "page": 21,
    "category": "Installation & Visibility",
    "tag": "Mounting Height",
    "text": "The maximum height above the ground shall be measured from the highest point and the minimum height from the lowest point of the apparent surface in the direction of the reference axis.",
    "test": "Measure heights of each function from the highest and lowest points of the apparent surface."
  },
  {
    "id": "R-0019",
    "reg": "UN R48",
    "para": "5.8.1",
    "page": 21,
    "category": "Installation & Visibility",
    "tag": "Mounting Height",
    "text": "For the purposes of reducing the geometric visibility angles, the position of a lamp with regard to height above the ground shall be measured from the H plane.",
    "test": "Measure height of the H plane (centre of reference) above ground when applying the 750 mm reduction rule."
  },
  {
    "id": "R-0020",
    "reg": "UN R48",
    "para": "5.8.3",
    "page": 21,
    "category": "Installation & Visibility",
    "tag": "Lateral Position",
    "text": "The position, as regards width, will be determined from that edge of the apparent surface in the direction of the reference axis which is the furthest from the median longitudinal plane of the vehicle when referred to the overall width, and from the inner edges of the apparent surface when referred to the distance between lamps.",
    "test": "Measure lateral positions from the outermost/inner apparent surface edges."
  },
  {
    "id": "R-0021",
    "reg": "UN R48",
    "para": "5.9",
    "page": 21,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In the absence of specific instructions, the photometric characteristics (e.g. intensity, colour, apparent surface, etc.) of a lamp shall not be intentionally varied during the period when the lamp is switched ON.",
    "test": "Observe each function while ON and verify no intentional variation of intensity, colour or apparent surface."
  },
  {
    "id": "R-0022",
    "reg": "UN R48",
    "para": "5.10.1",
    "page": 21,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "Red light emitted by a lamp fitted on the rear of the vehicle shall not be visible from the front of the vehicle.",
    "test": "Check from the front of the vehicle that no red light from the rear lamps is visible."
  },
  {
    "id": "R-0023",
    "reg": "UN R48",
    "para": "5.10.4.1",
    "page": 22,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "For the visibility of red light towards the front of a vehicle, there shall be no direct visibility of the apparent surface of a red lamp if viewed by an observer moving within Zone 1 in a transverse plane situated 25 m in front of the vehicle (see Annex 4).",
    "test": "Observer moves within Zone 1 in a plane 25 m ahead of the vehicle and confirms no direct visibility of red rear lamp apparent surfaces."
  },
  {
    "id": "R-0024",
    "reg": "UN R48",
    "para": "Annex 4",
    "page": 106,
    "category": "Installation & Visibility",
    "tag": "Lateral Position",
    "text": "Zone 1 explored by the eye of the observer is bounded in height by two horizontal planes 1 m and 2.2 m respectively above the ground, and in width by two vertical planes forming to the front an angle of 15\u00b0 outwards from the vehicle's median longitudinal plane passing through the point(s) of contact of vertical planes delimiting the vehicle's overall width.",
    "test": "Set up observation zone 1 m to 2.2 m height and 15\u00b0 outwards from overall width contact points for the red light visibility check."
  },
  {
    "id": "R-0025",
    "reg": "UN R48",
    "para": "5.10.4.3",
    "page": 22,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In case of doubt, the requirement shall be deemed fulfilled if the luminous intensity of the red light emitted to the front, as verified during type approval of the lamps, is not more than 0.25 cd per lamp taking into account the influence of the vehicle body if applicable.",
    "test": "Review lamp approval photometry for forward red light \u2264 0.25 cd per lamp."
  },
  {
    "id": "R-0026",
    "reg": "UN R48",
    "para": "5.11",
    "page": 22,
    "category": "Markings",
    "tag": "Electrical Connection",
    "text": "The electrical connections shall be such that the front and rear position lamps, the end-outline marker lamps, if they exist, the side-marker lamps, if they exist, and the rear registration plate lamp can only be switched ON and OFF simultaneously.",
    "test": "Operate the position lamp switch and verify rear position lamps switch ON/OFF simultaneously with front position, side-marker and registration plate lamps."
  },
  {
    "id": "R-0027",
    "reg": "UN R48",
    "para": "5.15",
    "page": 23,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of the light emitted by the reversing lamp shall be white.",
    "test": "Verify reversing lamp approval marking/colour measurement is white."
  },
  {
    "id": "R-0028",
    "reg": "UN R48",
    "para": "5.15",
    "page": 23,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of the light emitted by the stop lamp shall be red.",
    "test": "Verify stop lamp colour is red."
  },
  {
    "id": "R-0029",
    "reg": "UN R48",
    "para": "5.15",
    "page": 23,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of the light emitted by the rear position lamp shall be red.",
    "test": "Verify rear position lamp colour is red."
  },
  {
    "id": "R-0030",
    "reg": "UN R48",
    "para": "5.15",
    "page": 23,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of the rear retro-reflector, non-triangular, shall be red.",
    "test": "Verify rear retro-reflector colour is red."
  },
  {
    "id": "R-0031",
    "reg": "UN R48",
    "para": "5.17",
    "page": 24,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Any lamp may be installed on movable components provided that the conditions specified in paragraphs 5.18., 5.19. and 5.20. are fulfilled.",
    "test": "If any part of the rear lamp is on a tailgate/boot lid, verify compliance with 5.18 to 5.20."
  },
  {
    "id": "R-0032",
    "reg": "UN R48",
    "para": "5.18.1",
    "page": 25,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "Rear position lamps and rear retro-reflectors may be installed on movable components only if at all fixed positions of the movable components the lamps on the movable components meet all the position, geometric visibility, colorimetric and photometric requirements for those lamps.",
    "test": "Check position, visibility, colour and photometry of lamps on movable components at all fixed positions."
  },
  {
    "id": "R-0033",
    "reg": "UN R48",
    "para": "5.18.3",
    "page": 25,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "Where additional lamps for the rear position lamp or rear retro-reflector functions are fitted and are switched ON when the movable component is in any fixed open position, these additional lamps shall satisfy all the position, geometric visibility and photometric requirements applicable to the lamps installed on the movable component.",
    "test": "With the movable component open, verify additional lamps meet position, visibility and photometric requirements."
  },
  {
    "id": "R-0034",
    "reg": "UN R48",
    "para": "5.19",
    "page": 25,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "When the movable components are in a position other than a \"normal position of use\", the devices installed on them shall not cause undue discomfort to road users.",
    "test": "Open the movable component and verify the rear lamp does not cause glare or discomfort."
  },
  {
    "id": "R-0035",
    "reg": "UN R48",
    "para": "5.20",
    "page": 25,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "When a lamp is installed on a movable component and the movable component is in the \"normal position(s) of use\", the lamp shall always return to the position(s) specified by the manufacturer in accordance with this Regulation.",
    "test": "Cycle the movable component and verify the lamp returns to its specified position."
  },
  {
    "id": "R-0036",
    "reg": "UN R48",
    "para": "5.21",
    "page": 25,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The apparent surface in the direction of the reference axis of rear position lamps and retro-reflectors shall not be hidden more than 50 per cent by any movable component, with or without a light-signalling device installed on it, in any fixed position different from the \"normal position of use\".",
    "test": "Measure obscured apparent surface proportion with movable components in each fixed open position."
  },
  {
    "id": "R-0037",
    "reg": "UN R48",
    "para": "5.21.1",
    "page": 26,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "If the 50 per cent requirement is not practicable, additional lamps satisfying all the position, geometric visibility, colorimetric and photometric requirements for the above indicated lamps shall be switched ON when the apparent surface in the direction of the reference axis of these lamps is more than 50 per cent hidden by the movable component.",
    "test": "Verify additional compliant lamps switch ON when more than 50% of the apparent surface is hidden."
  },
  {
    "id": "R-0038",
    "reg": "UN R48",
    "para": "5.21.3",
    "page": 26,
    "category": "Markings",
    "tag": "Retro-reflection",
    "text": "Paragraph 5.21.2. (remark and user notice alternative) does not apply to retro-reflectors.",
    "test": "Confirm retro-reflector obscuration is solved by 5.21 or 5.21.1 and not by a notice."
  },
  {
    "id": "R-0039",
    "reg": "UN R48",
    "para": "5.22",
    "page": 26,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "With the exception of retro-reflectors, a lamp even bearing an approval mark is deemed not to be present when it cannot be made to operate by the sole installation of a light source and/or a fuse.",
    "test": "Verify each rear lamp function is wired and operable without additional components other than light source/fuse."
  },
  {
    "id": "R-0040",
    "reg": "UN R48",
    "para": "5.24",
    "page": 26,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "Any temporary fail-safe replacement of the light-signalling function of a rear position lamp is allowed, provided that the replacement function in case of a failure is similar in colour, main intensity and position to the function that has ceased to operate and provided that the replacement device remains operational in its original safety function.",
    "test": "Simulate rear position lamp failure and verify replacement function colour, intensity and position and that the replacing device keeps its own function."
  },
  {
    "id": "R-0041",
    "reg": "UN R48",
    "para": "5.27.1",
    "page": 27,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The voltage supplied at the terminals of stop lamps and rear position lamps which, according to their type approval documentation, have been tested by the application of a special power supply/electronic light source control gear, or in a secondary operating mode or at a voltage requested by the applicant, shall not exceed the voltage specified for the relevant devices or functions as they have been approved.",
    "test": "Measure terminal voltage at constant vehicle operating voltage and compare with approved voltage."
  },
  {
    "id": "R-0042",
    "reg": "UN R48",
    "para": "5.27.2",
    "page": 27,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In all other cases the voltage at the terminals of the device(s) or function(s) shall not exceed 13.5 V (12 Volt-Systems) or 28 V (24 Volt-Systems) or 6.75 V (6 Volt-Systems) by more than 3 per cent.",
    "test": "Measure terminal voltage of stop and rear position lamps and verify \u2264 nominal +3%."
  },
  {
    "id": "R-0043",
    "reg": "UN R48",
    "para": "5.27.3",
    "page": 27,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The provisions of paragraphs 5.27.1. and 5.27.2. shall not apply to devices which include an electronic light source control gear, or a variable intensity control being part of the device, or only light source(s) approved according to UN Regulation No. 128.",
    "test": "Check device documentation for integrated electronic control gear to determine exemption."
  },
  {
    "id": "R-0044",
    "reg": "UN R48",
    "para": "5.28.1",
    "page": 27,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "There shall be no obstacle on the inside of the angles of geometric visibility to the propagation of light from any part of the apparent surface of the lamp observed from infinity; no account is taken of obstacles already presented when the lamp was type-approved.",
    "test": "Check visibility angles of installed lamps for obstruction by vehicle bodywork."
  },
  {
    "id": "R-0045",
    "reg": "UN R48",
    "para": "5.28.3",
    "page": 27,
    "category": "Photometric",
    "tag": "Photometric Provision",
    "text": "If, when the lamp is installed, any part of the apparent surface of the lamp is hidden by any further parts of the vehicle, proof shall be furnished that the part of the lamp not hidden by obstacles still conforms to the photometric values prescribed for the approval of the device.",
    "test": "Where partial obscuration exists, review photometric proof of the unobscured part."
  },
  {
    "id": "R-0046",
    "reg": "UN R48",
    "para": "5.28.4",
    "page": 28,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "When the vertical angle of geometric visibility below the horizontal may be reduced to 5\u00b0 (lamp at less than 750 mm above the ground), the photometric field of measurements of the installed optical unit may be reduced to 5\u00b0 below the horizontal.",
    "test": "For lamps below 750 mm verify photometric field coverage at least down to 5\u00b0 below horizontal."
  },
  {
    "id": "R-0047",
    "reg": "UN R48",
    "para": "5.29",
    "page": 28,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "A LED module does not need to be replaceable, if so stated in the communication sheet of the component type approval.",
    "test": "Check the component approval communication sheet for non-replaceable LED module statement."
  },
  {
    "id": "R-0048",
    "reg": "UN R48",
    "para": "5.30",
    "page": 28,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "All lamps (devices) shall, where applicable, be type approved according to the corresponding device Regulations as specified in the relevant subparagraphs of paragraph 6 of this Regulation when installed on a vehicle.",
    "test": "Verify approval markings on each rear lamp function."
  },
  {
    "id": "R-0049",
    "reg": "UN R48",
    "para": "5.30.1",
    "page": 28,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case of light-signalling lamps incorporating a manufacturer logo, the lamp shall be type approved according to the requirements of UN Regulation No. 148.",
    "test": "If a logo is incorporated, verify R148 approval of the lamp."
  },
  {
    "id": "R-0050",
    "reg": "UN R48",
    "para": "6.4.2.3",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Reversing lamp devices shall be type-approved according to the 00 or subsequent series of amendments to UN Regulation No. 23, or to the 00 or subsequent series of amendments to UN Regulation No. 148.",
    "test": "Check reversing lamp approval marking for R23 or R148."
  },
  {
    "id": "R-0051",
    "reg": "UN R48",
    "para": "6.4.4.2",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Reversing lamp in height: not less than 250 mm and not more than 1,200 mm above the ground.",
    "test": "Measure lowest and highest points of reversing lamp apparent surface above ground."
  },
  {
    "id": "R-0052",
    "reg": "UN R48",
    "para": "6.4.4.3",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Reversing lamp in length: at the rear of the vehicle.",
    "test": "Verify reversing lamp is mounted at the rear."
  },
  {
    "id": "R-0053",
    "reg": "UN R48",
    "para": "6.4.5.1",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "Reversing lamp devices installed at the rear of the vehicle shall have a vertical angle of geometric visibility \u03b1 = 15\u00b0 upwards and 5\u00b0 downwards.",
    "test": "Verify unobstructed visibility of the reversing lamp apparent surface from 15\u00b0 up to 5\u00b0 down."
  },
  {
    "id": "R-0054",
    "reg": "UN R48",
    "para": "6.4.5.1",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "Reversing lamp devices installed at the rear of the vehicle shall have a horizontal angle of geometric visibility \u03b2 = 45\u00b0 to right and to left if there is only one device.",
    "test": "With a single reversing lamp, verify visibility 45\u00b0 left and right."
  },
  {
    "id": "R-0055",
    "reg": "UN R48",
    "para": "6.4.5.1",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "Reversing lamp devices installed at the rear of the vehicle shall have a horizontal angle of geometric visibility \u03b2 = 45\u00b0 outwards and 30\u00b0 inwards if there are two.",
    "test": "With two reversing lamps, verify visibility 45\u00b0 outwards and 30\u00b0 inwards for each."
  },
  {
    "id": "R-0056",
    "reg": "UN R48",
    "para": "6.4.6.1",
    "page": 39,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Reversing lamp orientation: rearwards.",
    "test": "Verify reversing lamp reference axis points rearwards."
  },
  {
    "id": "R-0057",
    "reg": "UN R48",
    "para": "6.4.7.1",
    "page": 40,
    "category": "Installation & Visibility",
    "tag": "Electrical Connection",
    "text": "The electrical connections shall be such that the reversing lamp can be switched ON only if the reverse gear is engaged and if the device which controls the starting and stopping of the propulsion system is in such a position that operation of the propulsion system is possible.",
    "test": "Engage reverse with propulsion system enabled and verify lamp ON; verify no activation otherwise."
  },
  {
    "id": "R-0058",
    "reg": "UN R48",
    "para": "6.4.7.1",
    "page": 40,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The reversing lamp shall not switch ON or remain ON if either of the above conditions is not satisfied.",
    "test": "Disengage reverse or switch off propulsion system and verify reversing lamp switches OFF."
  },
  {
    "id": "R-0059",
    "reg": "UN R48",
    "para": "6.4.8",
    "page": 40,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "Reversing lamp tell-tale optional; however a tell-tale indicating failure is mandatory if required by the component regulation.",
    "test": "Check component approval for failure tell-tale requirement and verify its presence if required."
  },
  {
    "id": "R-0060",
    "reg": "UN R48",
    "para": "6.7.2",
    "page": 45,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The stop lamp devices shall be type-approved according to the 02 or subsequent series of amendments to UN Regulation No. 7, or to the 00 or subsequent series of amendments to UN Regulation No. 148.",
    "test": "Check stop lamp approval marking for R7 (02+) or R148."
  },
  {
    "id": "R-0061",
    "reg": "UN R48",
    "para": "6.7.4.1",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "For M1 category vehicles, for S1 or S2 categories devices that point on the apparent surface in the direction of the reference axis which is farthest from the vehicle's median longitudinal plane shall not be more than 400 mm from the extreme outer edge of the vehicle.",
    "test": "Measure distance from the outermost apparent surface point of each stop lamp to the vehicle extreme outer edge (\u2264400 mm)."
  },
  {
    "id": "R-0062",
    "reg": "UN R48",
    "para": "6.7.4.2.1",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "For S1 or S2 categories devices: above the ground, not less than 350 mm nor more than 1,500 mm (2,100 mm if the shape of the bodywork makes it impossible to keep within 1,500 mm and if the optional lamps are not installed).",
    "test": "Measure stop lamp apparent surface heights above ground."
  },
  {
    "id": "R-0063",
    "reg": "UN R48",
    "para": "6.7.4.4",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "For S1 or S2 categories devices in length: at the rear of the vehicle.",
    "test": "Verify stop lamps are mounted at the rear."
  },
  {
    "id": "R-0064",
    "reg": "UN R48",
    "para": "6.7.5",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "For S1 or S2 categories stop lamp devices the horizontal angle of geometric visibility shall be 45\u00b0 to the left and to the right of the longitudinal axis of the vehicle.",
    "test": "Verify unobstructed stop lamp visibility 45\u00b0 left and right."
  },
  {
    "id": "R-0065",
    "reg": "UN R48",
    "para": "6.7.5",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "For stop lamps of categories S1 and S2 mounted below 750 mm, the inward angle of 45\u00b0 may be reduced to 20\u00b0 under the H plane.",
    "test": "For stop lamps with H plane below 750 mm, verify inward visibility at least 20\u00b0 below H plane."
  },
  {
    "id": "R-0066",
    "reg": "UN R48",
    "para": "6.7.5",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "For S1 or S2 categories stop lamp devices the vertical angle of geometric visibility shall be 15\u00b0 above and below the horizontal.",
    "test": "Verify stop lamp visibility 15\u00b0 up and 15\u00b0 down."
  },
  {
    "id": "R-0067",
    "reg": "UN R48",
    "para": "6.7.5",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "Where a stop lamp is mounted below 750 mm, the downward angle of 15\u00b0 may be reduced to 5\u00b0.",
    "test": "For stop lamps below 750 mm, verify downward visibility at least 5\u00b0."
  },
  {
    "id": "R-0068",
    "reg": "UN R48",
    "para": "6.7.6",
    "page": 47,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Stop lamp orientation: towards the rear of the vehicle.",
    "test": "Verify stop lamp reference axis points rearwards."
  },
  {
    "id": "R-0069",
    "reg": "UN R48",
    "para": "6.7.7.1",
    "page": 47,
    "category": "Installation & Visibility",
    "tag": "Electrical Connection",
    "text": "All stop lamps shall be switched ON simultaneously when the braking system provides the relevant signal defined in UN Regulations Nos. 13 and 13-H.",
    "test": "Apply the service brake and verify all stop lamps illuminate simultaneously."
  },
  {
    "id": "R-0070",
    "reg": "UN R48",
    "para": "6.7.7.2",
    "page": 47,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The stop lamps need not function if the device which starts and/or stops the propulsion system is in a position that makes it impossible for the propulsion system to operate.",
    "test": "Check stop lamp behaviour with propulsion system disabled (operation permitted but not required)."
  },
  {
    "id": "R-0071",
    "reg": "UN R48",
    "para": "6.10.2",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Two rear position lamps, type-approved according to the 02 or subsequent series of amendments to UN Regulation No. 7, or to the 00 or subsequent series of amendments to UN Regulation No. 148.",
    "test": "Count rear position lamps and check approval markings."
  },
  {
    "id": "R-0072",
    "reg": "UN R48",
    "para": "6.10.4.1",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Lateral Position",
    "text": "Rear position lamp in width: that point on the apparent surface in the direction of the reference axis which is farthest from the vehicle's median longitudinal plane shall not be more than 400 mm from the extreme outer edge of the vehicle.",
    "test": "Measure outermost apparent surface point to extreme outer edge (\u2264400 mm)."
  },
  {
    "id": "R-0073",
    "reg": "UN R48",
    "para": "6.10.4.2",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Rear position lamp in height: above the ground, not less than 350 mm nor more than 1,500 mm (2,100 mm if the shape of the bodywork makes it impossible to keep within 1,500 mm and if the optional lamps are not installed).",
    "test": "Measure rear position lamp apparent surface heights."
  },
  {
    "id": "R-0074",
    "reg": "UN R48",
    "para": "6.10.4.3",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Rear position lamp in length: the rear of the vehicle.",
    "test": "Verify rear position lamps mounted at the rear."
  },
  {
    "id": "R-0075",
    "reg": "UN R48",
    "para": "6.10.5.1",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "The rear position lamps shall have a horizontal angle of geometric visibility of 45\u00b0 inwards and 80\u00b0 outwards.",
    "test": "Verify unobstructed visibility 45\u00b0 inwards and 80\u00b0 outwards."
  },
  {
    "id": "R-0076",
    "reg": "UN R48",
    "para": "6.10.5.1",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "Where a rear position lamp is mounted below 750 mm, the inward angle of 45\u00b0 may be reduced to 20\u00b0 under the H plane.",
    "test": "For lamps below 750 mm verify inward visibility at least 20\u00b0 below H plane."
  },
  {
    "id": "R-0077",
    "reg": "UN R48",
    "para": "6.10.5.1",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "The rear position lamps shall have a vertical angle of geometric visibility of 15\u00b0 above and below the horizontal.",
    "test": "Verify visibility 15\u00b0 up and down."
  },
  {
    "id": "R-0078",
    "reg": "UN R48",
    "para": "6.10.5.1",
    "page": 50,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "Where a rear position lamp is mounted below 750 mm, the downward angle of 15\u00b0 may be reduced to 5\u00b0.",
    "test": "For lamps below 750 mm verify downward visibility at least 5\u00b0."
  },
  {
    "id": "R-0079",
    "reg": "UN R48",
    "para": "6.10.5.2",
    "page": 51,
    "category": "Markings",
    "tag": "Geometric Visibility",
    "text": "For M1 category vehicles, as an alternative, only if a rear side-marker lamp is installed on the vehicle, the rear position lamps shall have a horizontal angle of geometric visibility of 45\u00b0 outwards to 45\u00b0 inwards (inward angle may be reduced to 20\u00b0 under the H plane where mounted below 750 mm).",
    "test": "If the alternative is used, confirm rear side-marker lamp presence and visibility 45\u00b0 outwards/45\u00b0 inwards."
  },
  {
    "id": "R-0080",
    "reg": "UN R48",
    "para": "6.10.5.2",
    "page": 51,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "Under the alternative, the rear position lamps shall have a vertical angle of geometric visibility of 15\u00b0 above and below the horizontal (downward angle may be reduced to 5\u00b0 where mounted below 750 mm).",
    "test": "Verify vertical visibility 15\u00b0 up and down (5\u00b0 down if below 750 mm)."
  },
  {
    "id": "R-0081",
    "reg": "UN R48",
    "para": "6.10.5.2",
    "page": 51,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "To be considered visible, the rear position lamp shall provide an unobstructed view of the apparent surface of at least 12.5 square centimetres.",
    "test": "Measure unobstructed apparent surface area at visibility angle limits (\u226512.5 cm\u00b2)."
  },
  {
    "id": "R-0082",
    "reg": "UN R48",
    "para": "6.10.5.2",
    "page": 51,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "When determining the unobstructed view of the apparent surface of the rear position lamp, the illuminating surface area of any retro-reflector that does not transmit light shall be excluded.",
    "test": "Exclude the non-transmitting retro-reflector area from the 12.5 cm\u00b2 calculation."
  },
  {
    "id": "R-0083",
    "reg": "UN R48",
    "para": "6.10.6",
    "page": 51,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Rear position lamp orientation: rearwards.",
    "test": "Verify rear position lamp reference axis points rearwards."
  },
  {
    "id": "R-0084",
    "reg": "UN R48",
    "para": "6.10.7",
    "page": 51,
    "category": "Installation & Visibility",
    "tag": "Electrical Connection",
    "text": "Rear position lamp electrical connections shall be in accordance with paragraph 5.11.",
    "test": "Verify simultaneous switching with front position lamps and other 5.11 lamps."
  },
  {
    "id": "R-0085",
    "reg": "UN R48",
    "para": "6.10.8",
    "page": 51,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Closed-circuit tell-tale mandatory for rear position lamps; it shall be combined with that of the front position lamps.",
    "test": "Verify a closed-circuit tell-tale shared with front position lamps."
  },
  {
    "id": "R-0086",
    "reg": "UN R48",
    "para": "6.10.8",
    "page": 51,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "A tell-tale indicating failure of the rear position lamps is mandatory if required by the component Regulation.",
    "test": "Check component approval for failure tell-tale requirement."
  },
  {
    "id": "R-0087",
    "reg": "UN R48",
    "para": "6.19.7.5",
    "page": 61,
    "category": "Installation & Visibility",
    "tag": "Electrical Connection",
    "text": "When daytime running lamps are switched ON, the rear position lamps shall be switched ON; however they may be switched OFF and remain OFF as long as the ambient light conditions outside the vehicle are above 7,000 lux.",
    "test": "Activate DRL in low ambient light and verify rear position lamps ON; above 7,000 lux OFF permitted."
  },
  {
    "id": "R-0088",
    "reg": "UN R48",
    "para": "6.14.2",
    "page": 55,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Two rear retro-reflectors, type-approved according to the requirements concerning Class IA or IB retro-reflectors in the 02 or subsequent series of amendments to UN Regulation No. 3, or in the 00 or subsequent series of amendments to UN Regulation No. 150.",
    "test": "Count rear retro-reflectors and check Class IA/IB approval marking."
  },
  {
    "id": "R-0089",
    "reg": "UN R48",
    "para": "6.14.4.1",
    "page": 55,
    "category": "Photometric",
    "tag": "Lateral Position",
    "text": "Rear retro-reflector in width: that point on the illuminating surface which is farthest from the vehicle's median longitudinal plane shall not be more than 400 mm from the extreme outer edge of the vehicle.",
    "test": "Measure outermost illuminating surface point to extreme outer edge (\u2264400 mm)."
  },
  {
    "id": "R-0090",
    "reg": "UN R48",
    "para": "6.14.4.2",
    "page": 55,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Rear retro-reflector in height: above the ground, not less than 250 mm nor more than 900 mm (not more than 1,200 mm if grouped with any rear lamp(s), 1,500 mm if the shape of the bodywork makes it impossible to keep within 900 mm or 1,200 mm respectively).",
    "test": "Measure retro-reflector height; for grouped rear lamp verify \u22641,200 mm."
  },
  {
    "id": "R-0091",
    "reg": "UN R48",
    "para": "6.14.4.3",
    "page": 55,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Rear retro-reflector in length: at the rear of the vehicle.",
    "test": "Verify retro-reflectors at the rear."
  },
  {
    "id": "R-0092",
    "reg": "UN R48",
    "para": "6.14.5",
    "page": 55,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "The rear retro-reflector shall have a horizontal angle of geometric visibility of 30\u00b0 inwards and outwards.",
    "test": "Verify retro-reflector visibility 30\u00b0 inwards and outwards."
  },
  {
    "id": "R-0093",
    "reg": "UN R48",
    "para": "6.14.5",
    "page": 55,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "The rear retro-reflector shall have a vertical angle of geometric visibility of 10\u00b0 above and below horizontal.",
    "test": "Verify retro-reflector visibility 10\u00b0 up and down."
  },
  {
    "id": "R-0094",
    "reg": "UN R48",
    "para": "6.14.5",
    "page": 55,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "Where a retro-reflector is mounted below 750 mm, the downward angle of 10\u00b0 may be reduced to 5\u00b0.",
    "test": "For retro-reflectors below 750 mm verify downward visibility at least 5\u00b0."
  },
  {
    "id": "R-0095",
    "reg": "UN R48",
    "para": "6.14.6",
    "page": 55,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Rear retro-reflector orientation: rearwards.",
    "test": "Verify retro-reflector reference axis points rearwards."
  },
  {
    "id": "R-0096",
    "reg": "UN R48",
    "para": "6.14.7",
    "page": 56,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The illuminating surface of the retro-reflector may have parts in common with the apparent surface of any other lamp situated at the rear.",
    "test": "Where shared surfaces exist, confirm each function still meets its requirements."
  },
  {
    "id": "R-0097",
    "reg": "UN R48",
    "para": "Annex 9 1.2.1",
    "page": 114,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "The angles of geometric visibility shall be checked in accordance with paragraph 2.10.7.; the values measured for the angles shall be such that the individual specifications applicable to each lamp are fulfilled except that the limits of the angles may have an allowance corresponding to the \u00b13\u00b0 variation permitted in paragraph 5.3.",
    "test": "In conformity of production, measure visibility angles and accept within \u00b13\u00b0 allowance."
  },
  {
    "id": "R-0098",
    "reg": "UN R48",
    "para": "Annex 9 1.2.2",
    "page": 114,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "The visibility of red light towards the front shall be checked in accordance with paragraph 5.10.",
    "test": "In conformity of production, repeat the red light forward visibility check."
  },
  {
    "id": "R-0099",
    "reg": "UN R148",
    "para": "3.2.2",
    "page": 4,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "When two or more lamps are part of the same unit of grouped, combined or reciprocally incorporated lamps, approval may be granted only if each of these lamps satisfy the provisions set out in this Regulation or in another Regulation.",
    "test": "Confirm that each function in the rear lamp assembly (rear position, stop, reversing, retro-reflector) holds or meets the requirements of an applicable UN Regulation."
  },
  {
    "id": "R-0100",
    "reg": "UN R148",
    "para": "3.2.2",
    "page": 4,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Lamps not satisfying the provisions of any of those Regulations shall not be part of such unit of grouped, combined or reciprocally incorporated lamps.",
    "test": "Review the assembly bill of functions and confirm that no non-compliant lamp is integrated in the unit."
  },
  {
    "id": "R-0101",
    "reg": "UN R148",
    "para": "3.3.1.1",
    "page": 6,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "Every device belonging to an approved type shall comprise a space of sufficient size for the approval marking and other markings as defined in paragraphs 3.3.3.2. to 3.3.3.6.",
    "test": "Inspect the drawings and the sample for a reserved marking area large enough for all required markings."
  },
  {
    "id": "R-0102",
    "reg": "UN R148",
    "para": "3.3.1.1.1",
    "page": 6,
    "category": "Markings",
    "tag": "Markings Provision",
    "text": "All markings shall be clearly legible and indelible.",
    "test": "Visually inspect the markings and perform a rub test to confirm legibility and indelibility."
  },
  {
    "id": "R-0103",
    "reg": "UN R148",
    "para": "3.3.1.2",
    "page": 6,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "With regard to the size of the approval marking the value for \"a\" shall be at least 5 mm.",
    "test": "Measure the approval mark dimension \"a\" on the sample and confirm it is \u2265 5 mm."
  },
  {
    "id": "R-0104",
    "reg": "UN R148",
    "para": "3.3.2.1",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the approval mark, i.e. a circle surrounding the letter \"E\" followed by the distinguishing number of the country which has granted approval.",
    "test": "Inspect the marking for a circle enclosing the letter E and the country number."
  },
  {
    "id": "R-0105",
    "reg": "UN R148",
    "para": "3.3.2.2",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the four to six-digit sequential number, being part of the approval number.",
    "test": "Verify that a 4 to 6 digit sequential approval number is present in the marking."
  },
  {
    "id": "R-0106",
    "reg": "UN R148",
    "para": "3.2.3.2",
    "page": 4,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "This sequential number shall be placed close to the approval mark.",
    "test": "Inspect the marking layout to confirm the sequential number is located adjacent to the E-circle."
  },
  {
    "id": "R-0107",
    "reg": "UN R148",
    "para": "3.3.2.3",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the symbols identifying the light signalling lamps prescribed in paragraph 3.2.4.",
    "test": "Check that the symbols R1/R2, S1/S2 and AR, as applicable, are present in the marking."
  },
  {
    "id": "R-0108",
    "reg": "UN R148",
    "para": "3.3.2.4",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the number of this Regulation followed by the letter 'R' and the two digits indicating the series of amendments in force at the time of issue of the approval.",
    "test": "Verify that the marking shows \"148R\" followed by the series digits (e.g. 01)."
  },
  {
    "id": "R-0109",
    "reg": "UN R148",
    "para": "3.3.2.5.1",
    "page": 7,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "On lamps which cannot be mounted on either side of the vehicle indiscriminately, a horizontal arrow showing in which position the lamp is to be mounted.",
    "test": "For a handed lamp, confirm that a horizontal arrow is present in the marking."
  },
  {
    "id": "R-0110",
    "reg": "UN R148",
    "para": "3.3.2.5.1.1",
    "page": 7,
    "category": "Markings",
    "tag": "Markings Provision",
    "text": "The arrow shall be directed outwards from the vehicle in the case of front or rear position lamps, front or rear end-outline marker lamps.",
    "test": "Check that the arrow associated with the rear position lamp points outboard when the lamp is in its mounted orientation."
  },
  {
    "id": "R-0111",
    "reg": "UN R148",
    "para": "3.3.2.5.1.1",
    "page": 7,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "The arrow shall be directed outwards from the vehicle in the case of reversing lamps in case of reduced light distribution of two reversing lamps.",
    "test": "If the reversing lamp is approved for pair-only installation, check that the arrow points outboard."
  },
  {
    "id": "R-0112",
    "reg": "UN R148",
    "para": "3.3.2.5.2",
    "page": 7,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "If applicable, to the right side of the symbol mentioned in paragraph 3.2.4., the additional letter \"D\", on lamps which may be used as part of an assembly of two independent lamps.",
    "test": "If the lamp is approved as a \"D\" lamp, verify that the letter D appears to the right of the function symbol."
  },
  {
    "id": "R-0113",
    "reg": "UN R148",
    "para": "3.3.2.5.3",
    "page": 8,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "On lamps with reduced light distribution, a vertical arrow starting from a horizontal segment and directed downwards.",
    "test": "For a lamp approved with a mounting height \u2264 750 mm, check that the downward arrow symbol is present."
  },
  {
    "id": "R-0114",
    "reg": "UN R148",
    "para": "3.3.3.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "Lamps shall bear the approval marking.",
    "test": "Inspect the sample for the presence of the approval marking."
  },
  {
    "id": "R-0115",
    "reg": "UN R148",
    "para": "3.3.3.2",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "Lamps shall bear the trade name or mark of the applicant.",
    "test": "Inspect the sample for the applicant's trade name or mark."
  },
  {
    "id": "R-0116",
    "reg": "UN R148",
    "para": "3.3.3.4",
    "page": 8,
    "category": "Markings",
    "tag": "Photometric Intensity",
    "text": "Lamps shall bear marking of the rated voltage(s) (i.e. 6V, 12V or 24V) or the range of voltage, in the case of lamps with an electronic light source control gear; and/or a variable luminous intensity control; and/or a secondary operating mode; and/or non-replaceable light sources.",
    "test": "Verify that the rated voltage (e.g. 12V) or the voltage range is marked on the LED lamp."
  },
  {
    "id": "R-0117",
    "reg": "UN R148",
    "para": "3.3.3.5",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "In case replaceable light source module(s) is/are used, the light source module(s) shall bear the trade name or mark of the applicant.",
    "test": "Inspect each replaceable LED module for the applicant's trade name or mark."
  },
  {
    "id": "R-0118",
    "reg": "UN R148",
    "para": "3.3.3.5",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "In case replaceable light source module(s) is/are used, the light source module(s) shall bear the specific identification code of the module, comprising the starting letters \"MD\" followed by the approval mark without the circle, and, in case several non-identical light source modules are used, followed by additional symbols or characters.",
    "test": "Check the module marking for the format \"MD E.. nnnnn\" plus distinguishing characters where several non-identical modules are used."
  },
  {
    "id": "R-0119",
    "reg": "UN R148",
    "para": "3.3.3.5",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval mark on the light source module does not have to be the same as the one on the lamp in which the module is used, but both marks shall be from the same applicant.",
    "test": "Compare the module and lamp approval marks and confirm they belong to the same applicant."
  },
  {
    "id": "R-0120",
    "reg": "UN R148",
    "para": "3.3.3.5",
    "page": 8,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case replaceable light source module(s) is/are used, the light source module(s) shall bear the rated voltage(s) or the range of voltage.",
    "test": "Inspect the module for the rated voltage or voltage range marking."
  },
  {
    "id": "R-0121",
    "reg": "UN R148",
    "para": "3.3.3.5",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "In case replaceable light source module(s) is/are used, the lamp shall bear the specific identification code of the module.",
    "test": "Inspect the lamp housing for the module identification code."
  },
  {
    "id": "R-0122",
    "reg": "UN R148",
    "para": "3.3.3.5",
    "page": 8,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case replaceable light source module(s) is/are used, the lamp shall bear the rated voltage(s) or the range of voltage.",
    "test": "Inspect the lamp housing for the rated voltage or voltage range marking."
  },
  {
    "id": "R-0123",
    "reg": "UN R148",
    "para": "3.3.3.6",
    "page": 8,
    "category": "Markings",
    "tag": "Photometric Intensity",
    "text": "An electronic light source control gear or variable luminous intensity control being part of the lamp, but not included into the lamp body, shall be marked with its identification number and the name of the manufacturer.",
    "test": "If an external LED driver is part of the lamp, verify that it carries its identification number and the manufacturer name."
  },
  {
    "id": "R-0124",
    "reg": "UN R148",
    "para": "3.3.4.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall be placed on an inner or outer part (transparent or not) of the lamp which is not designed to be separated from the transparent part of the lamp emitting the light.",
    "test": "Verify that the marking is located on the outer lens or on a part permanently joined to it."
  },
  {
    "id": "R-0125",
    "reg": "UN R148",
    "para": "3.3.4.2",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "In any case the approval marking shall be visible when the lamp is fitted on the vehicle or when a movable part such as the hood or boot lid or a door is opened.",
    "test": "Check the marking visibility with the lamp installed on the vehicle, opening the boot lid if necessary."
  },
  {
    "id": "R-0126",
    "reg": "UN R148",
    "para": "3.3.4.3",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "If the outer lens of a device is designed to be separated from the main body, the approval marking shall be placed on both, the detachable lens and the main body.",
    "test": "If the lens is detachable, inspect both the lens and the housing for the approval marking."
  },
  {
    "id": "R-0127",
    "reg": "UN R148",
    "para": "3.3.4.4",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "In case an outer lens is used for several devices and bearing different approval markings, the main body of each device shall bear only the approval marking of the function(s) of that device.",
    "test": "Where a common lens is used, inspect each device body to confirm it carries only its own function markings."
  },
  {
    "id": "R-0128",
    "reg": "UN R148",
    "para": "3.3.4.5",
    "page": 9,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking and the markings in paragraphs 3.3.3.2., 3.3.3.3., 3.3.3.4., 3.3.3.5. (b) and 3.3.3.6. shall be affixed on the lamp.",
    "test": "Inspect the lamp to confirm that these markings are on the lamp itself."
  },
  {
    "id": "R-0129",
    "reg": "UN R148",
    "para": "3.3.4.6",
    "page": 9,
    "category": "Markings",
    "tag": "Markings Provision",
    "text": "The markings in paragraphs 3.3.3.5.(a) shall be affixed on the component.",
    "test": "Inspect the light source module to confirm that its markings are on the module itself."
  },
  {
    "id": "R-0130",
    "reg": "UN R148",
    "para": "3.3.4.7",
    "page": 9,
    "category": "Markings",
    "tag": "Markings Provision",
    "text": "The markings in paragraphs 3.3.3.2., 3.3.3.3. (a), 3.3.3.4., 3.3.3.5. and 3.3.3.6. do not need to fulfil the requirements of paragraph 3.3.4.2.",
    "test": "Note that the visibility-when-fitted check is not applied to these markings."
  },
  {
    "id": "R-0131",
    "reg": "UN R148",
    "para": "3.3.5.1",
    "page": 9,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "Where grouped, combined or reciprocally incorporated lamps have been found to comply with the requirements of several UN Regulations, a single approval mark with the four to six-digit sequential number may be affixed, located anywhere on the grouped, combined or reciprocally incorporated lamps, provided that it is visible after their installation.",
    "test": "If a single mark is used, check its visibility with the rear lamp installed."
  },
  {
    "id": "R-0132",
    "reg": "UN R148",
    "para": "3.3.5.1.2",
    "page": 9,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "No part of the grouped, combined or reciprocally incorporated lamps that transmits light can be removed without at the same time removing the approval mark.",
    "test": "Check that no light-transmitting part can be detached without also removing the single approval mark."
  },
  {
    "id": "R-0133",
    "reg": "UN R148",
    "para": "3.3.5.2",
    "page": 9,
    "category": "Markings",
    "tag": "Colour & Chromaticity",
    "text": "The size of the components of a single approval mark shall not be less than the minimum size required for the smallest of the individual marks by the pertinent UN Regulations under which approval has been granted.",
    "test": "Measure the single mark components and compare them with the smallest minimum size required by R148 and the retro-reflector Regulation."
  },
  {
    "id": "R-0134",
    "reg": "UN R148",
    "para": "4.1",
    "page": 10,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Each lamp submitted for approval shall conform to the requirements set forth in paragraphs 4. and 5.",
    "test": "Perform the full set of paragraph 4 and paragraph 5 tests on each function."
  },
  {
    "id": "R-0135",
    "reg": "UN R148",
    "para": "4.2",
    "page": 10,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The requirements contained in sections 5 \"General specifications\" and 6 \"Individual specifications\" (and in the Annexes referenced in the said sections) of UN Regulation No. 48 and its series of amendments in force at the time of application for the lamp type approval shall apply; the requirements pertinent to each lamp and to the category/ies of vehicle on which the lamp is intended to be installed shall be applied, where its verification at the moment of lamp type approval is feasible.",
    "test": "Verify the applicable R48 installation-related requirements (e.g. visibility, apparent surface) for M1 where feasible at component level."
  },
  {
    "id": "R-0136",
    "reg": "UN R148",
    "para": "4.3",
    "page": 10,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "The lamps must be so designed and constructed that in normal conditions of use, and notwithstanding the vibrations to which they may be subjected in such use, their satisfactory operation remains assured.",
    "test": "Assess the design robustness and confirm that operation remains correct after vibration exposure."
  },
  {
    "id": "R-0137",
    "reg": "UN R148",
    "para": "4.3",
    "page": 10,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The lamps must be so designed and constructed that in normal conditions of use, and notwithstanding the vibrations to which they may be subjected in such use, they retain the characteristics prescribed by this Regulation.",
    "test": "Re-check photometry and colour after vibration exposure to confirm the characteristics are retained."
  },
  {
    "id": "R-0138",
    "reg": "UN R148",
    "para": "4.5.3.1",
    "page": 10,
    "category": "Installation & Visibility",
    "tag": "Failure Indication",
    "text": "In the case of a rear position lamp reciprocally incorporated with a stop lamp, these functions shall either be provided by multiple light sources (for instance, a double filament light source); or be intended for use in a vehicle equipped with a tell-tale indicating failure for the lamps, and in either case a note shall be made within the communication document.",
    "test": "Check the light source architecture of the reciprocally incorporated rear position/stop function, or the tell-tale declaration, and the communication form note."
  },
  {
    "id": "R-0139",
    "reg": "UN R148",
    "para": "4.5.5",
    "page": 11,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The internal structure of the optical components and/or the texture of the outer lens inside of the apparent surface of a lamp (function) may incorporate only one manufacturer logo, provided that all requirements for the specific function of this Regulation are fulfilled.",
    "test": "If a logo is present in the rear position lamp, confirm that it is the only logo and that the function remains compliant."
  },
  {
    "id": "R-0140",
    "reg": "UN R148",
    "para": "4.5.5",
    "page": 11,
    "category": "Markings",
    "tag": "Markings Provision",
    "text": "Irrespective of the marking requirements in paragraph 3.3., only the logo of the brand name of the vehicle manufacturer or the body manufacturer is allowed.",
    "test": "Check the vehicle manufacturer statement confirming the logo is the official brand logo."
  },
  {
    "id": "R-0141",
    "reg": "UN R148",
    "para": "4.5.5",
    "page": 11,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The enclosed light emitting surface of the logo (incorporating transparent and non-transparent components of the logo) of such a lamp in the direction of the reference axis shall not exceed 100 cm2.",
    "test": "Measure the projected logo light emitting surface along the reference axis and confirm it is \u2264 100 cm\u00b2."
  },
  {
    "id": "R-0142",
    "reg": "UN R148",
    "para": "4.5.5",
    "page": 11,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Notwithstanding the requirements of paragraph 5.5.2. of UN Regulation No. 48, the logo light emitting surface does not have to be symmetrical by itself.",
    "test": "Note that a symmetry check of the logo itself is not required."
  },
  {
    "id": "R-0143",
    "reg": "UN R148",
    "para": "4.5.5",
    "page": 11,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Stop lamps, direction indicator lamps, and reversing lamps shall not incorporate a logo.",
    "test": "Inspect the apparent surfaces of the stop and reversing lamps to confirm no logo is incorporated."
  },
  {
    "id": "R-0144",
    "reg": "UN R148",
    "para": "4.6.1.1",
    "page": 11,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "In a single lamp containing more than one light source, a group of light sources, wired so that the failure of any one of them causes all of them to stop emitting light, shall be considered to be one light source.",
    "test": "Analyse the LED circuit wiring to identify the series groups treated as one light source."
  },
  {
    "id": "R-0145",
    "reg": "UN R148",
    "para": "4.6.1.2",
    "page": 11,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In case of failure of any one light source in a single lamp containing more than one light source, the light intensity complies with the minimum intensity required in the pertinent table of standard light distribution as shown in Annex 3 and when all light sources are illuminated the maximum intensities shall not be exceeded; or a signal for activation of a tell-tale indicating failure is produced.",
    "test": "Simulate a single LED/group failure and measure the minimum intensities, or verify that a failure tell-tale signal is generated."
  },
  {
    "id": "R-0146",
    "reg": "UN R148",
    "para": "4.7.1",
    "page": 12,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The lamp shall only be equipped with replaceable light source(s) approved according to UN Regulations Nos. 37, 99 and/or 128, provided that no restriction on the use is made at the time of application for type approval, and/or light source module(s) and/or non-replaceable light source(s).",
    "test": "Review the light source design (LED modules/non-replaceable LEDs) against the permitted types."
  },
  {
    "id": "R-0147",
    "reg": "UN R148",
    "para": "4.7.2.3",
    "page": 13,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Light Signalling Devices shall not generate radiated or power line disturbances, which cause a malfunction of other electric/electronic systems of the vehicle.",
    "test": "Perform EMC emission testing (radiated and conducted) of the lamp electronics."
  },
  {
    "id": "R-0148",
    "reg": "UN R148",
    "para": "4.7.2.4",
    "page": 13,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case of replaceable light source module(s), the design of the light source module(s) shall be such that it can only be fitted in the designated and correct position.",
    "test": "Attempt to fit the module in incorrect orientations and confirm that only the correct position is possible."
  },
  {
    "id": "R-0149",
    "reg": "UN R148",
    "para": "4.7.2.4",
    "page": 13,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case of replaceable light source module(s), the design of the light source module(s) shall be such that it can only be removed with the use of tool(s).",
    "test": "Attempt removal by hand and confirm that a tool is required."
  },
  {
    "id": "R-0150",
    "reg": "UN R148",
    "para": "4.7.2.4",
    "page": 13,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case of replaceable light source module(s), the design of the light source module(s) shall be such that it is tamperproof.",
    "test": "Inspect the module for tamperproof construction (no access to internals without damage)."
  },
  {
    "id": "R-0151",
    "reg": "UN R148",
    "para": "4.7.2.4",
    "page": 13,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In case of replaceable light source module(s), regardless of the use of tool(s), it is not interchangeable with any replaceable UN approved light source; and/or any other replaceable light source module having different characteristics that is located in the same lamp housing.",
    "test": "Attempt to interchange the module with approved light sources and other modules in the housing and confirm it is not possible."
  },
  {
    "id": "R-0152",
    "reg": "UN R148",
    "para": "4.7.2.4",
    "page": 13,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "When the light source module is removed and replaced by another module provided by the applicant and bearing the same light source module identification code, the photometric requirements of device shall be met.",
    "test": "Replace the module with another module of the same code and repeat the photometric measurements."
  },
  {
    "id": "R-0153",
    "reg": "UN R148",
    "para": "4.8.1.2",
    "page": 13,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In the case of a lamp equipped with light source module(s) or non-replaceable light source(s), all measurements shall be made with the light source(s) present in the lamp.",
    "test": "Perform the photometric and colorimetric tests with the original LED modules fitted."
  },
  {
    "id": "R-0154",
    "reg": "UN R148",
    "para": "4.8.1.5",
    "page": 13,
    "category": "Photometric",
    "tag": "Radiated Immunity",
    "text": "In the case where the lamp may be installed on the vehicle in more than one or in a field of different positions the photometric measurements shall be repeated for each position or for the extreme positions of the field of the reference axis specified by the manufacturer.",
    "test": "Repeat the photometry at each declared mounting position or at the extreme positions."
  },
  {
    "id": "R-0155",
    "reg": "UN R148",
    "para": "4.8.1.8.3",
    "page": 14,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The intensity requirement for a particular direction of observation shall be deemed to be satisfied if that requirement is met in a direction deviating by not more than one-quarter of a degree from the direction of observation.",
    "test": "In case of dispute, accept compliance within \u00b10.25\u00b0 of the measurement direction."
  },
  {
    "id": "R-0156",
    "reg": "UN R148",
    "para": "4.8.1.9",
    "page": 14,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The limits of the apparent surface in the direction of the reference axis of a light-signalling lamp shall be determined.",
    "test": "Determine and document the apparent surface outline of each function along the reference axis."
  },
  {
    "id": "R-0157",
    "reg": "UN R148",
    "para": "4.8.2",
    "page": 14,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Unless otherwise specified, the voltage supplied at the lamp shall be either 6.75 V (6 Volt-Systems), 13.5 V (12 Volt-Systems) or 28 V (24 Volt-Systems).",
    "test": "Supply the lamp at 13.5 V (12 V system) during photometric testing."
  },
  {
    "id": "R-0158",
    "reg": "UN R148",
    "para": "4.8.2.1",
    "page": 14,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In case of a lamp controlled by an electronic light source control gear or a variable intensity control, the lamp shall be operated as specified by the applicant.",
    "test": "Operate the lamp via its driver under the applicant-specified conditions."
  },
  {
    "id": "R-0159",
    "reg": "UN R148",
    "para": "4.8.2.2.1",
    "page": 14,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In case of a lamp not controlled by an electronic light source control gear or a variable intensity control, in the case of light source module(s) or non-replaceable light source(s) the lamp shall be operated as specified by the applicant.",
    "test": "Operate the LED lamp at the applicant-specified conditions during the tests."
  },
  {
    "id": "R-0160",
    "reg": "UN R148",
    "para": "4.8.3.1",
    "page": 14,
    "category": "COP",
    "tag": "Photometric Intensity",
    "text": "If not otherwise specified, the intensity of light emitted by each of the two samples supplied shall, on the reference axis (HV), be not less than the minimum specified in the table of the pertinent function in paragraph 5.",
    "test": "Measure the HV intensity of both samples for each function and compare it with the minimum."
  },
  {
    "id": "R-0161",
    "reg": "UN R148",
    "para": "4.8.3.1",
    "page": 14,
    "category": "COP",
    "tag": "Photometric Intensity",
    "text": "If not otherwise specified, the intensity of light emitted by each of the two samples supplied shall, in no direction where the lamp is visible, exceed the maximum specified in the table of the pertinent function in paragraph 5.",
    "test": "Goniometer scan of both samples confirming that no direction exceeds the maximum."
  },
  {
    "id": "R-0162",
    "reg": "UN R148",
    "para": "4.8.3.1",
    "page": 14,
    "category": "COP",
    "tag": "Photometric Intensity",
    "text": "If not otherwise specified, the intensity of light emitted by each of the two samples supplied shall, outside the reference axis, be not less than the product of the minimum specified in the table of the pertinent function in paragraph 5. by the percentage specified in the pertinent light distribution figure reproduced in Annex 3 for each direction in question, or be not less than the intensity value as specified in the pertinent light distribution figure reproduced in Annex 3 for each direction in question.",
    "test": "Measure each grid point of the Annex 3 distribution and compare it with the minimum \u00d7 percentage or the specified cd value."
  },
  {
    "id": "R-0163",
    "reg": "UN R148",
    "para": "4.8.3.1",
    "page": 14,
    "category": "COP",
    "tag": "Geometric Visibility",
    "text": "If not otherwise specified, the intensity of light emitted by each of the two samples supplied shall, within the angles of geometric visibility defined in the tables in Annex 2, be not less than the minimum specified in the table of the pertinent function in paragraph 5.",
    "test": "Measure the intensity throughout the Annex 2 visibility field and confirm it is not below the minimum."
  },
  {
    "id": "R-0164",
    "reg": "UN R148",
    "para": "4.8.3.1",
    "page": 14,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The provisions of the relevant paragraphs of Annex 3 on local variations of intensity shall be observed.",
    "test": "Check the intensities between grid points for local variation compliance."
  },
  {
    "id": "R-0165",
    "reg": "UN R148",
    "para": "4.8.3.1.1",
    "page": 15,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "In order to verify the visibility of red light towards the front and/or white light towards the rear of a vehicle required in UN Regulation No. 48, the applicant may request an additional test, to show that in the angular field from 165\u00b0 to 180\u00b0 outboard in horizontal direction and -2.5\u00b0 to +5\u00b0 in vertical direction, the maximum intensity is not more than 2.5\u221910-1 cd.",
    "test": "If requested, measure the intensity in the 165\u00b0\u2013180\u00b0 H, -2.5\u00b0 to +5\u00b0 V field and confirm it is \u2264 0.25 cd."
  },
  {
    "id": "R-0166",
    "reg": "UN R148",
    "para": "4.8.3.5",
    "page": 16,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "If a rear position lamp is reciprocally incorporated with a stop lamp producing either steady or variable luminous intensity, the ratio between the luminous intensities actually measured of the two lamps when turned on simultaneously and the intensity of the rear position lamp when turned on alone should be at least 5:1 in the field delimited by the straight horizontal lines passing through \u00b15\u00b0 V and the straight vertical lines passing through \u00b110\u00b0 H of the light distribution table.",
    "test": "Measure stop+position vs position-only intensities in the \u00b110\u00b0 H / \u00b15\u00b0 V field and confirm a ratio \u2265 5:1."
  },
  {
    "id": "R-0167",
    "reg": "UN R148",
    "para": "4.8.3.5",
    "page": 16,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "If one or both of the two reciprocally incorporated lamps contain(s) more than one light source and is (are) considered as a single lamp, the values to be considered are those obtained with all sources in operation.",
    "test": "Perform the ratio measurement with all LEDs of each function operating."
  },
  {
    "id": "R-0168",
    "reg": "UN R148",
    "para": "4.8.3.6",
    "page": 16,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "Tests for compliance of the luminous intensities shall be carried out according to Annex 8.",
    "test": "Apply the Annex 8 timing procedure for the intensity measurements."
  },
  {
    "id": "R-0169",
    "reg": "UN R148",
    "para": "4.9",
    "page": 16,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of the light emitted shall be measured inside the field of the light distribution grid defined for the specific function in the relevant paragraph of Annex 3, applying the test procedure described in paragraph 4.8.",
    "test": "Measure chromaticity across the Annex 3 grid of each function under paragraph 4.8 conditions."
  },
  {
    "id": "R-0170",
    "reg": "UN R148",
    "para": "4.9",
    "page": 16,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "Outside this field no sharp variation of colour shall be observed.",
    "test": "Visually check outside the grid field for any abrupt colour change."
  },
  {
    "id": "R-0171",
    "reg": "UN R148",
    "para": "4.9",
    "page": 16,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "For lamps equipped with non-replaceable light sources, the colorimetric characteristics should be verified with the light sources present in the lamp.",
    "test": "Perform the colour measurement with the original LEDs installed."
  },
  {
    "id": "R-0172",
    "reg": "UN R148",
    "para": "5.2.1",
    "page": 17,
    "category": "COP",
    "tag": "Photometric Intensity",
    "text": "The light emitted by each of the two samples supplied shall meet the requirements in Table 4 for luminous intensity and standard light distribution.",
    "test": "Measure both rear position lamp samples against the Table 4 minimum/maximum values (R1: 4 cd min, 17 cd max; R2: 4 cd min, 42 cd max) and Figure A3-I."
  },
  {
    "id": "R-0173",
    "reg": "UN R148",
    "para": "5.2.1",
    "page": 17,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "A luminous intensity of 6.0\u2219101 cd shall be permitted for rear position lamps reciprocally incorporated with stop lamps below a plane forming an angle of 5\u00b0 with and downward from the horizontal plane.",
    "test": "For a reciprocally incorporated rear position/stop lamp, accept up to 60 cd below 5\u00b0D."
  },
  {
    "id": "R-0174",
    "reg": "UN R148",
    "para": "5.2.2",
    "page": 17,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "Rear position lamps shall meet the minimum luminous intensity within the angles of geometric visibility specified in Table 4 (5\u221910-2 cd).",
    "test": "Measure throughout the Table A2-1 field and confirm \u2265 0.05 cd."
  },
  {
    "id": "R-0175",
    "reg": "UN R148",
    "para": "5.2.7",
    "page": 17,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of light emitted by the rear position lamp shall be red.",
    "test": "Measure the chromaticity of the rear position lamp and confirm it is within the red limits."
  },
  {
    "id": "R-0176",
    "reg": "UN R148",
    "para": "5.5.1",
    "page": 19,
    "category": "COP",
    "tag": "Photometric Intensity",
    "text": "The light emitted by each of the two samples supplied shall meet the requirements in Table 7 for luminous intensity and standard light distribution.",
    "test": "Measure both stop lamp samples against Table 7 (S1: 60\u2013260 cd; S2: 60\u2013730 cd) and Figure A3-I."
  },
  {
    "id": "R-0177",
    "reg": "UN R148",
    "para": "5.5.2",
    "page": 20,
    "category": "Photometric",
    "tag": "Geometric Visibility",
    "text": "Stop lamps shall meet the minimum luminous intensity within the angles of geometric visibility specified in Table 7.",
    "test": "Measure throughout the Table A2-1 field and confirm \u2265 0.3 cd (S2: 0.07 cd at night)."
  },
  {
    "id": "R-0178",
    "reg": "UN R148",
    "para": "5.5.7",
    "page": 20,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of light emitted by the stop lamp shall be red.",
    "test": "Measure the chromaticity of the stop lamp and confirm it is within the red limits."
  },
  {
    "id": "R-0179",
    "reg": "UN R148",
    "para": "5.8.1",
    "page": 23,
    "category": "COP",
    "tag": "Photometric Intensity",
    "text": "The light emitted by each of the two samples supplied shall meet the requirements in Table 10 for luminous intensity and standard light distribution.",
    "test": "Measure both reversing lamp samples against Table 10 (min 80 cd; max 300 cd at or above H, 600 cd down to 5\u00b0D, 8000 cd below 5\u00b0D) and Figure A3-V."
  },
  {
    "id": "R-0180",
    "reg": "UN R148",
    "para": "5.8.1",
    "page": 23,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In the case where the reversing lamp is intended to be installed on a vehicle exclusively in a pair of devices, the photometric intensity may be verified only up to an angle of 30\u00b0 inwards where a photometric value of at least 2.5\u2219101 cd shall be satisfied.",
    "test": "For pair-only approval, measure at 30\u00b0 inwards and confirm \u2265 25 cd."
  },
  {
    "id": "R-0181",
    "reg": "UN R148",
    "para": "5.8.7",
    "page": 23,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colour of light emitted by the reversing lamp shall be white.",
    "test": "Measure the chromaticity of the reversing lamp and confirm it is within the white limits."
  },
  {
    "id": "R-0182",
    "reg": "UN R148",
    "para": "Annex 2 Part A",
    "page": 32,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "Front/rear position lamps (A, R1, R2) shall have minimum horizontal angles of geometric visibility of 45\u00b0 inboard / 80\u00b0 outboard (20\u00b0/80\u00b0 reduced angles used only below the H-plane for lamps mounted with the H-plane below 750 mm).",
    "test": "Verify the minimum intensity across the horizontal field 45\u00b0 in / 80\u00b0 out."
  },
  {
    "id": "R-0183",
    "reg": "UN R148",
    "para": "Annex 2 Part A",
    "page": 32,
    "category": "Installation & Visibility",
    "tag": "Mounting Height",
    "text": "Front/rear position lamps (A, R1, R2) shall have minimum vertical angles of geometric visibility of 15\u00b0 above / 15\u00b0 below (15\u00b0/5\u00b0 for lamps installed with the H-plane at a mounting height of less than 750 mm).",
    "test": "Verify the minimum intensity across the vertical field 15\u00b0 up / 15\u00b0 down (or 5\u00b0 down)."
  },
  {
    "id": "R-0184",
    "reg": "UN R148",
    "para": "Annex 2 Part A",
    "page": 32,
    "category": "Installation & Visibility",
    "tag": "Geometric Visibility",
    "text": "Stop lamps (S1, S2) shall have minimum horizontal angles of geometric visibility of 45\u00b0 inboard / 45\u00b0 outboard (20\u00b0/45\u00b0 reduced angles used only below the H-plane for lamps mounted with the H-plane below 750 mm).",
    "test": "Verify the minimum intensity across the horizontal field 45\u00b0 in / 45\u00b0 out."
  },
  {
    "id": "R-0185",
    "reg": "UN R148",
    "para": "Annex 2 Part A",
    "page": 32,
    "category": "Installation & Visibility",
    "tag": "Mounting Height",
    "text": "Stop lamps (S1, S2) shall have minimum vertical angles of geometric visibility of 15\u00b0 above / 15\u00b0 below (15\u00b0/5\u00b0 for lamps installed with the H-plane at a mounting height of less than 750 mm).",
    "test": "Verify the minimum intensity across the vertical field 15\u00b0 up / 15\u00b0 down (or 5\u00b0 down)."
  },
  {
    "id": "R-0186",
    "reg": "UN R148",
    "para": "Annex 3 1.1",
    "page": 35,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "The values shown in Figures A3-I to A3-XV give, for the various directions of measurement, the minimum intensities as a percentage of the minimum intensities required, which shall be mathematically rounded down to three significant digits.",
    "test": "Compute the grid minima as percentage \u00d7 minimum, rounded down to 3 significant digits, and compare them with the measurements."
  },
  {
    "id": "R-0187",
    "reg": "UN R148",
    "para": "Annex 3 1.1",
    "page": 35,
    "category": "Photometric",
    "tag": "Mounting Height",
    "text": "In the case where rear position lamps or stop lamps of category S1, S2 are intended to be installed at a mounting height (using the H plane specified by the manufacturer) equal to or less than 750 mm above the ground, the photometric intensity is verified only up to an angle of 5\u00b0 downwards.",
    "test": "For a declared mounting height \u2264 750 mm, limit the downward photometric verification to 5\u00b0D."
  },
  {
    "id": "R-0188",
    "reg": "UN R148",
    "para": "Annex 3 1.2",
    "page": 35,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "Within the field of light distribution schematically shown as a grid, the light intensity in each direction of a part of the field formed by the grid lines shall meet at least the lowest minimum value being shown on the grid lines surrounding the questioned direction as a percentage.",
    "test": "Check intermediate directions within each grid cell against the lowest surrounding grid value."
  },
  {
    "id": "R-0189",
    "reg": "UN R148",
    "para": "Annex 3 1.2",
    "page": 35,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In the case of reversing lamps, if visual examination of a lamp appears to reveal substantial local variations of intensity, a check shall be made to ensure that no intensity measured between two of the directions of measurement is below 50 per cent of the lower minimum intensity of the two prescribed for these directions of measurement.",
    "test": "Where local variations are seen in the reversing lamp, measure between the points and confirm \u2265 50 % of the lower minimum."
  },
  {
    "id": "R-0190",
    "reg": "UN R148",
    "para": "Annex 3 2.1",
    "page": 36,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "The rear position lamps and stop lamps (S1, S2) shall meet the standard light distribution of Figure A3-I, the values giving the minimum intensities as a percentage of the minimum intensities required (Tables 4 and 7).",
    "test": "Measure the Figure A3-I grid for the rear position and stop functions."
  },
  {
    "id": "R-0191",
    "reg": "UN R148",
    "para": "Annex 3 2.5",
    "page": 38,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The reversing lamp shall meet the standard light distribution of Figure A3-V, the values giving the minimum intensities in cd for the various directions of measurement.",
    "test": "Measure the Figure A3-V points for the reversing lamp and compare them with the cd minima."
  },
  {
    "id": "R-0192",
    "reg": "UN R148",
    "para": "Annex 8 1.2.1",
    "page": 47,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "For reversing lamps using light source technologies other than incandescent technology only, the luminous intensities measured after 1 minute and after 10 minutes of operation, shall comply with the minimum and maximum requirements.",
    "test": "Measure the LED reversing lamp at 1 min and 10 min of operation and check the min/max limits."
  },
  {
    "id": "R-0193",
    "reg": "UN R148",
    "para": "Annex 8 1.2.2",
    "page": 47,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "For all other lamps using light source technologies other than incandescent technology only, the luminous intensities measured after 1 min and either after 30 minutes of operation, or after photometric stability has occurred shall comply with the minimum and maximum requirements.",
    "test": "Measure the LED rear position and stop lamps at 1 min and at 30 min/stability and check the min/max limits."
  },
  {
    "id": "R-0194",
    "reg": "UN R148",
    "para": "Annex 8 2.1",
    "page": 47,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The luminous intensity distribution of front and rear position lamps shall additionally be checked for compliance at 4 seconds after switch ON, reference coordinate HV.",
    "test": "Measure the HV intensity of the rear position lamp 4 s after switch-on, or apply the Annex 8 2.1.2 LED deemed-to-comply provision."
  },
  {
    "id": "R-0195",
    "reg": "UN R148",
    "para": "Annex 8 2.1",
    "page": 47,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The luminous intensity distribution of stop lamps shall additionally be checked for compliance at 0.2 seconds after switch ON, reference coordinate HV.",
    "test": "Measure the HV intensity of the stop lamp 0.2 s after switch-on, or apply the LED deemed-to-comply provision."
  },
  {
    "id": "R-0196",
    "reg": "UN R148",
    "para": "Annex 8 2.1",
    "page": 47,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The luminous intensity distribution of reversing lamps shall additionally be checked for compliance at 0.2 seconds after switch ON, reference coordinate HV.",
    "test": "Measure the HV intensity of the reversing lamp 0.2 s after switch-on, or apply the LED deemed-to-comply provision."
  },
  {
    "id": "R-0197",
    "reg": "UN R148",
    "para": "Annex 8 2.1.2",
    "page": 48,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "In case a lamp (function) uses LED technology only, a lamp (function) is deemed to comply with the corresponding intensity requirements at all points in time, if the values measured according to paragraph 1.2. are compliant.",
    "test": "Confirm the functions are LED-only and that the Annex 8 1.2 measurements are compliant."
  },
  {
    "id": "R-0198",
    "reg": "UN R148",
    "para": "6.1.3",
    "page": 27,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "No measured value deviates unfavourably by more than 20 per cent from the values prescribed in this Regulation; for the minimum values required throughout the fields specified in Annexes 2 and 3 the measured values shall correspond to the values shown in Table 12.",
    "test": "Perform photometric CoP tests on production samples and confirm unfavourable deviations of \u2264 20 % (Table 12 values for low minima)."
  },
  {
    "id": "R-0199",
    "reg": "UN R148",
    "para": "Annex 4 1.3",
    "page": 42,
    "category": "Photometric",
    "tag": "Photometric Provision",
    "text": "The chromaticity coordinates shall be complied with when tested under conditions of paragraph 4.9. of this Regulation.",
    "test": "Measure the chromaticity of production samples and confirm the red/white limits are met."
  },
  {
    "id": "R-0200",
    "reg": "UN R150",
    "para": "3.3.1.1",
    "page": 7,
    "category": "Markings",
    "tag": "Colour & Chromaticity",
    "text": "Every device belonging to an approved type shall comprise a space of sufficient size for the Unique Identifier as referred to in the 1958 Agreement and other markings as defined in paragraph 3.3.4.2. or, the approval marking and other markings as defined in paragraph 3.3.4.2.",
    "test": "Inspect the retro-reflector/lamp drawings and samples for a marking space large enough for the UI or approval marking and the other markings."
  },
  {
    "id": "R-0201",
    "reg": "UN R150",
    "para": "3.3.1.2",
    "page": 7,
    "category": "Markings",
    "tag": "Markings Provision",
    "text": "All markings shall be clearly legible and indelible.",
    "test": "Visually check legibility and perform a rub/indelibility check on the markings."
  },
  {
    "id": "R-0202",
    "reg": "UN R150",
    "para": "3.3.1.3",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "With regard to the size of the approval marking the value for \"a\" is defined in Table 1 (minimum \"a\" = 5 mm for Classes IA and IB).",
    "test": "Measure the approval marking dimension \"a\" and confirm it is at least 5 mm."
  },
  {
    "id": "R-0203",
    "reg": "UN R150",
    "para": "3.3.2.1",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the approval mark, i.e. a circle surrounding the letter \"E\" followed by the distinguishing number of the country which has granted approval.",
    "test": "Inspect the marking for the circle with letter E and country number."
  },
  {
    "id": "R-0204",
    "reg": "UN R150",
    "para": "3.3.2.2",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the four to six-digit sequential number being part of the approval number; this sequential number shall be placed close to the approval mark.",
    "test": "Verify the 4-6 digit sequential number is present and placed close to the E-circle."
  },
  {
    "id": "R-0205",
    "reg": "UN R150",
    "para": "3.3.2.3",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the symbols identifying the retro-reflective device prescribed in paragraph 3.2.5. (IA or IB).",
    "test": "Verify the class symbol IA or IB is marked on the device."
  },
  {
    "id": "R-0206",
    "reg": "UN R150",
    "para": "3.3.2.4",
    "page": 7,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking shall consist of the number of this Regulation followed by the letter \"R\" and the two digits indicating the series of amendments in force at the time of issue of the approval.",
    "test": "Verify the marking contains '150R' followed by the series digits (e.g. 01)."
  },
  {
    "id": "R-0207",
    "reg": "UN R150",
    "para": "3.3.3.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking as defined in paragraph 3.3.2. may be replaced by the Unique Identifier, if available; the Unique Identifier mark shall follow the format shown in Figure I.",
    "test": "If UI is used, check that its format matches Figure I and that it is accessible in the UN database."
  },
  {
    "id": "R-0208",
    "reg": "UN R150",
    "para": "3.3.4.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "Retro-reflective devices shall bear the trade name or mark of the applicant.",
    "test": "Inspect the sample for the trade name or mark of the applicant."
  },
  {
    "id": "R-0209",
    "reg": "UN R150",
    "para": "3.3.4.2.1",
    "page": 8,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "In case of a retro-reflector of Class IA or IB, retro-reflective devices shall bear the word \"TOP\" inscribed horizontally on the highest part of the illuminating surface, if such an indication is necessary to determine without ambiguity the angle or angles of rotation prescribed by the manufacturer.",
    "test": "Where rotation position is relevant, verify 'TOP' is inscribed horizontally on the highest part of the illuminating surface."
  },
  {
    "id": "R-0210",
    "reg": "UN R150",
    "para": "3.3.5.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The approval marking or the Unique Identifier and the markings in paragraphs 3.3.4. shall be clearly legible on the retroreflective device.",
    "test": "Visually inspect the device to confirm the approval marking/UI, trade name and TOP marking are clearly legible."
  },
  {
    "id": "R-0211",
    "reg": "UN R150",
    "para": "3.3.6.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "Where grouped, combined or reciprocally incorporated lamps have been found to comply with the requirements of several UN Regulations, a single approval mark with the four to six-digit sequential number or Unique Identifier may be affixed, located anywhere on the grouped, combined or reciprocally incorporated lamps, provided the conditions of paragraphs 3.3.6.1.1. and 3.3.6.1.2. are met.",
    "test": "If a single approval mark is used on the rear lamp, verify it covers all relevant Regulations and satisfies 3.3.6.1.1 and 3.3.6.1.2."
  },
  {
    "id": "R-0212",
    "reg": "UN R150",
    "para": "3.3.6.1.1",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "The single approval mark shall be visible after installation of the grouped, combined or reciprocally incorporated lamps.",
    "test": "Check on the installed rear lamp that the single approval mark remains visible."
  },
  {
    "id": "R-0213",
    "reg": "UN R150",
    "para": "3.3.6.1.2",
    "page": 8,
    "category": "Markings",
    "tag": "Approval Marking",
    "text": "No part of the grouped, combined or reciprocally incorporated lamps that transmits light can be removed without at the same time removing the approval mark with the four to six-digit sequential number or the Unique Identifier.",
    "test": "Review construction to confirm no light-transmitting part (e.g. outer lens, retro-reflector) is removable without removing the approval mark."
  },
  {
    "id": "R-0214",
    "reg": "UN R150",
    "para": "3.3.6.2",
    "page": 8,
    "category": "Markings",
    "tag": "Colour & Chromaticity",
    "text": "The size of the components of a single approval mark shall not be less than the minimum size required for the smallest of the individual marks by the pertinent UN Regulations under which approval has been granted.",
    "test": "Measure the single approval mark components and compare with the minimum sizes required by each pertinent Regulation."
  },
  {
    "id": "R-0215",
    "reg": "UN R150",
    "para": "Annex 2 1.2",
    "page": 25,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "With respect to photometric performances, the conformity of mass-produced retro-reflective devices shall not be contested if, when testing photometric performances of any retro-reflective device chosen at random no measured value deviates unfavourably by more than 20 per cent from the minimum values prescribed in this Regulation.",
    "test": "Measure RI of randomly selected production retro-reflectors and confirm no value is more than 20 % below the prescribed minimum."
  },
  {
    "id": "R-0216",
    "reg": "UN R150",
    "para": "Annex 2 1.3",
    "page": 25,
    "category": "Photometric",
    "tag": "Photometric Provision",
    "text": "The chromaticity coordinates shall be complied with.",
    "test": "Measure chromaticity of production samples and confirm they are within the red night-time colour limits."
  },
  {
    "id": "R-0217",
    "reg": "UN R150",
    "para": "4",
    "page": 10,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The requirements contained in sections 5. \"General specifications\" and 6. \"Individual specifications\" and in the Annexes referenced in the said sections of UN Regulation No. 48 in force at the time of application, pertinent to the retro-reflecting device and to the category of vehicle on which it is intended to be installed, shall be applied where their verification at the moment of retro-reflecting device type approval is feasible.",
    "test": "Verify the applicable UN R48 installation requirements for a rear retro-reflector on M1 vehicles that are checkable at component level (e.g. geometric visibility, shape) are met."
  },
  {
    "id": "R-0218",
    "reg": "UN R150",
    "para": "4.1.1",
    "page": 10,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Retro-reflective devices shall be so constructed that they function satisfactorily and will continue to do so in normal use.",
    "test": "Assess design and test results (environmental tests) for continued satisfactory function."
  },
  {
    "id": "R-0219",
    "reg": "UN R150",
    "para": "4.1.1",
    "page": 10,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Retro-reflective devices must not have any defect in design or manufacture that is detrimental to their efficient operation or to their maintenance in good condition.",
    "test": "Visually inspect samples and design for defects detrimental to operation or maintenance."
  },
  {
    "id": "R-0220",
    "reg": "UN R150",
    "para": "4.1.2",
    "page": 10,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The components of retro-reflective devices or parts thereof shall not be capable of being easily dismantled.",
    "test": "Attempt to dismantle the retro-reflector components by hand and confirm they cannot be easily separated."
  },
  {
    "id": "R-0221",
    "reg": "UN R150",
    "para": "4.1.4",
    "page": 10,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The outer surface of retro-reflective devices shall be easy to clean.",
    "test": "Inspect the outer lens/retro-reflector surface for ease of cleaning."
  },
  {
    "id": "R-0222",
    "reg": "UN R150",
    "para": "4.1.4",
    "page": 10,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "The surface shall not be rough and any protuberances they may exhibit shall not prevent easy cleaning.",
    "test": "Visually and tactilely check the outer surface for roughness and protuberances preventing cleaning."
  },
  {
    "id": "R-0223",
    "reg": "UN R150",
    "para": "4.1.5",
    "page": 11,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "There shall be no access to the inner surface of the retro-reflectors when in normal use.",
    "test": "Verify on the assembled lamp that the inner (prism) surface of the retro-reflector is not accessible."
  },
  {
    "id": "R-0224",
    "reg": "UN R150",
    "para": "4.1.6.1",
    "page": 11,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Retro-reflectors may consist of a combined retro-reflecting optical unit and filter, which must be so designed that they cannot be separated under normal conditions of use.",
    "test": "If a filter is used, confirm optical unit and filter cannot be separated under normal use."
  },
  {
    "id": "R-0225",
    "reg": "UN R150",
    "para": "4.1.6.2",
    "page": 11,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The colouring of retro-reflecting optical units and filters by means of paint or varnish is not permitted.",
    "test": "Verify by material specification and inspection that the red colour is obtained in the mass (tinted PMMA), not by paint or varnish."
  },
  {
    "id": "R-0226",
    "reg": "UN R150",
    "para": "4.2.1.2",
    "page": 11,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "For testing the colour of the retro-reflective device, the device shall be illuminated by CIE Standard Illuminant A, with an angle of divergence of 1/3\u00b0 and an illumination angle of \u03b21 = \u03b22 = 0\u00b0 or, if this produces a colourless surface reflection, an angle as specified in Annex 4, Part 1, paragraph 1.1.",
    "test": "Set up colorimetric measurement with Illuminant A, 1/3\u00b0 divergence and \u03b21 = \u03b22 = 0\u00b0 (or \u03b21 = -5\u00b0 if mirror effect)."
  },
  {
    "id": "R-0227",
    "reg": "UN R150",
    "para": "4.2.1.2",
    "page": 11,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "The trichromatic coordinates of the reflected luminous intensity shall be within the limits for the night-time colour of the light retro-reflected from that device, as defined in UN Regulation No. 48.",
    "test": "Measure trichromatic coordinates and confirm they fall within the R48 red night-time retro-reflected colour limits."
  },
  {
    "id": "R-0228",
    "reg": "UN R150",
    "para": "5.1.1",
    "page": 11,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Every retro-reflector of the Classes IA and IB, when tested according to paragraph 5.1.7., shall meet the dimensions and shape requirements set forth in Annex 5.",
    "test": "Visually inspect shape and dimensions against Annex 5 paragraph 1."
  },
  {
    "id": "R-0229",
    "reg": "UN R150",
    "para": "5.1.1",
    "page": 11,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "Every retro-reflector of the Classes IA and IB, when tested according to paragraph 5.1.7., shall meet the photometric and colorimetric requirements as specified in paragraphs 5.1.4. to 5.1.5.",
    "test": "Perform photometric and colorimetric measurements per 5.1.4 and 5.1.5."
  },
  {
    "id": "R-0230",
    "reg": "UN R150",
    "para": "5.1.1",
    "page": 11,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "Every retro-reflector of the Classes IA and IB, when tested according to paragraph 5.1.7., shall meet the physical and mechanical requirements set forth in paragraph 5.1.7., depending on the nature of the materials and construction of the retro-reflective devices.",
    "test": "Run the test sequence of Table 4 (heat, water, fuels, oils, corrosion, rear face, stability, weathering) and check pass criteria."
  },
  {
    "id": "R-0231",
    "reg": "UN R150",
    "para": "5.1.3.1",
    "page": 11,
    "category": "COP",
    "tag": "Colour & Chromaticity",
    "text": "After the heat resistance test described in Part 1 of Annex 6, and at least one hour after this test, the samples shall be examined as to their colorimetric characteristics in paragraph 5.1.5. and RI in paragraph 5.1.4., for an angle of divergence of 20' and an illumination angle \u03b21 = \u03b22 = 0\u00b0 or, if necessary, in the position defined in Part 1 of Annex 4, paragraphs 1.1. and 1.2.",
    "test": "After heat test and \u22651 h rest, measure colour and RI at 20' and \u03b21 = \u03b22 = 0\u00b0 on all ten samples."
  },
  {
    "id": "R-0232",
    "reg": "UN R150",
    "para": "5.1.3.2.1",
    "page": 12,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "After undergoing the tests referred to in paragraph 5.1.3.1., the retro-reflectors in each group must have a colour which satisfies the conditions laid down in paragraph 5.1.5.",
    "test": "After each test group, measure/inspect colour and confirm compliance with 5.1.5."
  },
  {
    "id": "R-0233",
    "reg": "UN R150",
    "para": "5.1.3.2.2",
    "page": 12,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "After undergoing the tests referred to in paragraph 5.1.3.1., the retro-reflectors in each group must have a RI which satisfies the conditions laid down in paragraph 5.1.4.; the verification shall be performed only for an angle of divergence of 20' and an illumination angle of \u03b21 = \u03b22 = 0\u00b0 or, if necessary, in all positions specified in Part 1 of Annex 4, paragraphs 1.1. and 1.2.",
    "test": "After each test group, measure RI at 20' and \u03b21 = \u03b22 = 0\u00b0 and compare with Table 3 minimum."
  },
  {
    "id": "R-0234",
    "reg": "UN R150",
    "para": "5.1.4.2",
    "page": 12,
    "category": "Photometric",
    "tag": "Photometric Provision",
    "text": "In the case where more than one or a range of different axis of reference are specified by the manufacturer, the photometric measurements shall be repeated making reference each time to a different axis of reference or to the extreme axis of reference of the range specified by the manufacturer.",
    "test": "Repeat RI measurements for each declared reference axis or the extreme axes of the declared range."
  },
  {
    "id": "R-0235",
    "reg": "UN R150",
    "para": "5.1.4.3",
    "page": 12,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "For photometric measurements, only the illuminating surface defined by the planes contiguous to the outermost parts of the optical system of the retro-reflective device as indicated by the manufacturer and contained within a circle of 200 mm diameter for Class IA or IB shall be considered.",
    "test": "Confirm the measured illuminating surface lies within a 200 mm diameter circle."
  },
  {
    "id": "R-0236",
    "reg": "UN R150",
    "para": "5.1.4.3",
    "page": 12,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The illuminating surface itself shall be limited to 100 cm2 though the surfaces of the retro-reflecting optical units need not necessarily attain this area.",
    "test": "Mask the illuminating surface to not more than 100 cm\u00b2 for photometric measurement."
  },
  {
    "id": "R-0237",
    "reg": "UN R150",
    "para": "5.1.4.4.1",
    "page": 12,
    "category": "Photometric",
    "tag": "Photometric Intensity",
    "text": "When measured as described in paragraph 3 of Part 1 of Annex 4, the RI values for red retro-reflectors must be equal to or greater than those in Table 3, expressed in millicandelas per lux, for the angles of divergence and illumination shown.",
    "test": "Measure RI of red IA/IB retro-reflector at 20' and 1\u00b030' for the Table 3 illumination angles and confirm values are at or above the minima (e.g. 300 mcd/lx at 20', 0\u00b0/0\u00b0)."
  },
  {
    "id": "R-0238",
    "reg": "UN R150",
    "para": "5.1.4.4.1",
    "page": 12,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "RI values lower than those shown in the last two columns of Table 3 are not permissible within the solid angle having the centre of reference as its apex and bounded by the planes intersecting along the following lines: (\u03b21 = \u00b110\u00b0, \u03b22 = 0\u00b0) (\u03b21 = \u00b15\u00b0, \u03b22 = \u00b120\u00b0).",
    "test": "Scan RI within the defined solid angle and confirm no value falls below the corresponding limits."
  },
  {
    "id": "R-0239",
    "reg": "UN R150",
    "para": "5.1.4.5",
    "page": 13,
    "category": "Photometric",
    "tag": "Mounting Height",
    "text": "In the case where a retro-reflector of Class IA or Class IB is intended to be installed with its H plane at a mounting height less than 750 mm above the ground, the RI values are verified only up to an angle of 5\u00b0 downwards.",
    "test": "If declared mounting height < 750 mm, verify downward RI only up to 5\u00b0 below horizontal."
  },
  {
    "id": "R-0240",
    "reg": "UN R150",
    "para": "5.1.5.1",
    "page": 13,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The testing of the colour for retro-reflector (night-time colour) shall be carried out according to the method described in paragraph 4.2.1.",
    "test": "Perform night-time colour measurement per paragraph 4.2.1 conditions."
  },
  {
    "id": "R-0241",
    "reg": "UN R150",
    "para": "5.1.5.2",
    "page": 13,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The trichromatic coordinates of the reflected luminous flux must be within the limits for the night-time colours red, amber or white as specified in UN Regulation No. 48.",
    "test": "Measure chromaticity of the red retro-reflector and confirm it lies within the R48 red night-time limits."
  },
  {
    "id": "R-0242",
    "reg": "UN R150",
    "para": "Annex 4 Part 1 1.1",
    "page": 28,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "When the RI of a retro-reflective device is measured for an angle \u03b2 of \u03b21 = \u03b22 = 0\u00b0, it shall be ascertained whether any mirror effect is produced by slightly turning the device; if there is any such effect, a reading shall be taken with an angle \u03b2 of \u03b21 = -5\u00b0, \u03b22 = 0\u00b0.",
    "test": "Slightly rotate the device at \u03b2 = 0\u00b0/0\u00b0 to check for mirror effect and if present measure at \u03b21 = -5\u00b0."
  },
  {
    "id": "R-0243",
    "reg": "UN R150",
    "para": "Annex 4 Part 1 1.2",
    "page": 28,
    "category": "Markings",
    "tag": "Retro-reflection",
    "text": "With an illumination angle of \u03b21 = \u03b22 = 0\u00b0 and an angle of divergence of 20', retro-reflective devices which are not marked \"TOP\" shall be rotated about their axes of reference to the position of minimum RI, which must conform to the value specified in paragraph 5. of this Regulation.",
    "test": "For devices without TOP marking, rotate to the minimum RI position at 20' and 0\u00b0/0\u00b0 and confirm the value meets Table 3."
  },
  {
    "id": "R-0244",
    "reg": "UN R150",
    "para": "Annex 4 Part 1 1.2",
    "page": 28,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "When the RI is measured for the other angles of illumination and divergence, the retro-reflective device shall be placed in the position corresponding to this value of \u03b5; if the specified values are not attained, the device may be rotated about its axis of reference \u00b15\u00b0 from that position.",
    "test": "Measure other angles at the minimum-RI \u03b5 position, allowing \u00b15\u00b0 rotation if needed, and confirm compliance."
  },
  {
    "id": "R-0245",
    "reg": "UN R150",
    "para": "Annex 4 Part 1 1.3",
    "page": 28,
    "category": "Markings",
    "tag": "Retro-reflection",
    "text": "With an illumination angle of \u03b21 = \u03b22 = 0\u00b0 and an angle of divergence of 20', retro-reflective devices marked \"TOP\" shall be rotated about their axes \u00b15\u00b0; the RI must not fall below the prescribed value in any position assumed by the device during this rotation.",
    "test": "For TOP-marked devices, rotate \u00b15\u00b0 and confirm RI never falls below the minimum."
  },
  {
    "id": "R-0246",
    "reg": "UN R150",
    "para": "Annex 4 Part 1 1.4",
    "page": 28,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "If for the direction \u03b21 = \u03b22 = 0\u00b0, and for \u03b5 = 0\u00b0 the RI exceeds the specified value by 50 per cent or more, all measurements for all angles of illumination and divergence shall be made for \u03b5 = 0\u00b0.",
    "test": "If RI at 0\u00b0/0\u00b0, \u03b5 = 0\u00b0 is \u2265150 % of the minimum, perform all measurements at \u03b5 = 0\u00b0."
  },
  {
    "id": "R-0247",
    "reg": "UN R150",
    "para": "Annex 4 Part 1 3.3",
    "page": 30,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "For testing the retro-reflection the retro-reflective devices shall be illuminated with a CIE Standard Illuminant A.",
    "test": "Confirm photometric measurement source is calibrated to CIE Standard Illuminant A."
  },
  {
    "id": "R-0248",
    "reg": "UN R150",
    "para": "Annex 5 1.1",
    "page": 33,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "The shape of the illuminating surfaces shall not be easily confused with the triangular shape, as prescribed for retro-reflectors mentioned in paragraph 2.1., from an observation distance of 10 metres.",
    "test": "Visually inspect the retro-reflector from 10 m to confirm it is not easily confused with a triangle."
  },
  {
    "id": "R-0249",
    "reg": "UN R150",
    "para": "Annex 6 Part 1 1",
    "page": 42,
    "category": "COP",
    "tag": "Retro-reflection",
    "text": "In the case of moulded plastics reflectors of Classes IA and IB, the retro-reflective device shall be kept for 48 consecutive hours in a dry atmosphere at a temperature of 65 \u00b0C \u00b1 2 \u00b0C after which the sample shall be allowed to cool for 1 hour at 23 \u00b0C \u00b1 2 \u00b0C.",
    "test": "Expose samples to 65 \u00b0C \u00b1 2 \u00b0C dry heat for 48 h then cool 1 h at 23 \u00b0C \u00b1 2 \u00b0C."
  },
  {
    "id": "R-0250",
    "reg": "UN R150",
    "para": "Annex 6 Part 1 3",
    "page": 42,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "After this test, no cracking or appreciable distortion of the retro-reflective device and, in particular, of its optical component must be visible.",
    "test": "Visually inspect after heat test for cracking or distortion of the retro-reflector optics."
  },
  {
    "id": "R-0251",
    "reg": "UN R150",
    "para": "Annex 6 Part 2 1.1",
    "page": 42,
    "category": "Environmental",
    "tag": "Retro-reflection",
    "text": "Retro-reflective devices whether part of a lamp or not shall be immersed for 10 minutes in water at a temperature of 50 \u00b0C \u00b1 5 \u00b0C, with the highest point of the illuminating surface 20 mm below the surface, repeated in the inverted position, and then immediately immersed in the same conditions in water at a temperature of 25 \u00b0C \u00b1 5 \u00b0C.",
    "test": "Perform water immersion at 50 \u00b0C \u00b1 5 \u00b0C (normal and inverted, 10 min each) followed by 25 \u00b0C \u00b1 5 \u00b0C immersion."
  },
  {
    "id": "R-0252",
    "reg": "UN R150",
    "para": "Annex 6 Part 2 1.2",
    "page": 42,
    "category": "Environmental",
    "tag": "Colour & Chromaticity",
    "text": "No water shall penetrate to the reflecting surface of the retro-reflecting optical unit; if visual inspection clearly reveals the presence of water, the device shall not be considered to have passed the test.",
    "test": "Inspect the prism/reflecting surface for water after immersion."
  },
  {
    "id": "R-0253",
    "reg": "UN R150",
    "para": "Annex 6 Part 2 1.3.1",
    "page": 42,
    "category": "Environmental",
    "tag": "Colour & Chromaticity",
    "text": "If visual inspection does not reveal the presence of water or in case of doubt, in the case of retro-reflectors the RI shall be measured by the method described in paragraph 5.1.3.2.2., the retro-reflective device being first lightly shaken to remove excess water from the outside.",
    "test": "In case of doubt, shake off excess water and measure RI at 20', 0\u00b0/0\u00b0 against Table 3."
  },
  {
    "id": "R-0254",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 1",
    "page": 43,
    "category": "Environmental",
    "tag": "Retro-reflection",
    "text": "As an alternative for Class IB retro-reflectors, at the request of the manufacturer, the moisture and dust tests shall be applied instead of the water penetration test.",
    "test": "If requested for an IB device, apply moisture spray and dust tests instead of immersion."
  },
  {
    "id": "R-0255",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 2.1.3",
    "page": 44,
    "category": "Environmental",
    "tag": "Colour & Chromaticity",
    "text": "The precipitation rate of the water spray at the device shall be 2.5 (+1.6/-0) mm/min as measured with a vertical cylindrical collector centred on the vertical axis of the rotating test platform.",
    "test": "Calibrate spray to 2.5 (+1.6/-0) mm/min with the specified collector."
  },
  {
    "id": "R-0256",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 2.2.3",
    "page": 44,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "If the retro-reflector is reciprocally incorporated or grouped with signalling or lighting functions, these functions shall be operated at design voltage according to a cycle of 5 min ON (in flashing mode, where appropriate), 55 min OFF.",
    "test": "Operate the rear position, stop and reversing lamps at design voltage on a 5 min ON / 55 min OFF cycle during spray."
  },
  {
    "id": "R-0257",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 2.2.4",
    "page": 44,
    "category": "Environmental",
    "tag": "Water Resistance",
    "text": "The water spray test shall last 12 hours (12 cycles of 5/55 min).",
    "test": "Confirm spray test duration of 12 h."
  },
  {
    "id": "R-0258",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 2.2.6",
    "page": 44,
    "category": "Environmental",
    "tag": "Colour & Chromaticity",
    "text": "Upon completion of the 1 hour drain period, no standing pool of water shall be allowed to be formed, or which can be formed by tapping or tilting the device; the RI shall be measured according to Part 1 of Annex 4 after having dried the exterior.",
    "test": "After draining, inspect interior for standing water (including after tapping/tilting) and measure RI."
  },
  {
    "id": "R-0259",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 2.3.3",
    "page": 44,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "The test dust used shall be fine powdered cement in accordance with standard ASTM C 150-84.",
    "test": "Verify test dust certificate to ASTM C 150-84."
  },
  {
    "id": "R-0260",
    "reg": "UN R150",
    "para": "Annex 6 Part 3 2.3.7",
    "page": 45,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "Upon completion of the dust exposure test, the exterior of the device shall be cleaned and dried and the RI measured according to the method specified in paragraph 5.1.3.2.2.",
    "test": "Clean exterior after dust test and measure RI at 20', 0\u00b0/0\u00b0 for compliance with Table 3."
  },
  {
    "id": "R-0261",
    "reg": "UN R150",
    "para": "Annex 6 Part 4 1",
    "page": 45,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "Retro-reflective devices must be so designed that they retain the prescribed photometric and colorimetric characteristics despite the humidity and corrosive influences to which they are normally exposed.",
    "test": "After corrosion test, measure RI and colour and confirm compliance."
  },
  {
    "id": "R-0262",
    "reg": "UN R150",
    "para": "Annex 6 Part 4 2",
    "page": 45,
    "category": "COP",
    "tag": "Retro-reflection",
    "text": "The retro-reflective device, or the lamp if the device is combined with a light, shall be subjected to the action of a saline mist for a period of 50 hours, comprising two periods of exposure of 24 hours each, separated by an interval of two hours during which the sample is allowed to dry.",
    "test": "Expose the lamp to salt mist 24 h + 2 h dry + 24 h per ISO 9227."
  },
  {
    "id": "R-0263",
    "reg": "UN R150",
    "para": "Annex 6 Part 4 3",
    "page": 45,
    "category": "Environmental",
    "tag": "Retro-reflection",
    "text": "In the case of retro-reflective devices with essential metal components susceptible to corrosion, the saline mist shall be produced by atomizing, at a temperature of 35 \u00b0C \u00b1 2 \u00b0C, a saline solution of 5 parts by weight of sodium chloride in 95 parts of distilled water containing not more than 0.02 per cent of impurities.",
    "test": "Verify salt mist parameters: 35 \u00b0C \u00b1 2 \u00b0C, 5 % NaCl solution with \u22640.02 % impurities."
  },
  {
    "id": "R-0264",
    "reg": "UN R150",
    "para": "Annex 6 Part 4 4.1",
    "page": 45,
    "category": "COP",
    "tag": "COP Provision",
    "text": "Immediately after completion of the test, the sample shall not show signs of excessive corrosion liable to impair the efficiency of the device.",
    "test": "Inspect the sample immediately after salt mist for excessive corrosion."
  },
  {
    "id": "R-0265",
    "reg": "UN R150",
    "para": "Annex 6 Part 5 3",
    "page": 45,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "In the case of moulded plastics reflectors of Classes IA and IB with an accessible mirror-backed rear face, after brushing with a hard nylon brush, a cotton cloth soaked in the 70 % n-heptane / 30 % toluol mixture shall be applied to the rear face for one minute.",
    "test": "Brush the rear face, apply fuel-soaked cloth for 1 min, dry and brush again."
  },
  {
    "id": "R-0266",
    "reg": "UN R150",
    "para": "Annex 6 Part 5 6",
    "page": 46,
    "category": "Installation & Visibility",
    "tag": "Colour & Chromaticity",
    "text": "The RI shall then be measured, according to paragraph 5.1.3.2.2., after the whole surface of the mirror-backed rear face has been covered with Indian ink.",
    "test": "Cover rear face with Indian ink and measure RI at 20', 0\u00b0/0\u00b0 for compliance with Table 3."
  },
  {
    "id": "R-0267",
    "reg": "UN R150",
    "para": "Annex 6 Part 6 3.1",
    "page": 46,
    "category": "COP",
    "tag": "Retro-reflection",
    "text": "The samples shall be exposed to accelerated artificial weathering in accordance with EN ISO 4892-2:2013 using the parameters given in Table A6-1, in case of retro-reflective devices for a period of 500 hours.",
    "test": "Expose samples for 500 h in a xenon tester per EN ISO 4892-2 with Table A6-1 parameters (102 min dry/18 min spray, 60 W/m\u00b2 broadband, BST 65 \u00b0C or BPT 63 \u00b0C, 50 % RH), then measure colour and RI."
  },
  {
    "id": "R-0268",
    "reg": "UN R150",
    "para": "Annex 7 Part 1 1",
    "page": 47,
    "category": "Photometric",
    "tag": "Retro-reflection",
    "text": "A test mixture of 70 vol. per cent of n-heptane and 30 vol. per cent of toluol shall be applied, the outer surface of the retro-reflective device and in particular the illuminating surface being lightly wiped with a cotton cloth soaked in the test mixture.",
    "test": "Wipe the illuminating surface with a cloth soaked in 70/30 n-heptane/toluol."
  },
  {
    "id": "R-0269",
    "reg": "UN R150",
    "para": "Annex 7 Part 1 1.1",
    "page": 47,
    "category": "Installation & Visibility",
    "tag": "Installation & Visibility Provision",
    "text": "After about five minutes, the surface must not show any apparent surface changes, except that slight surface cracks will not be objected to.",
    "test": "Inspect the surface after ~5 min for apparent surface changes."
  },
  {
    "id": "R-0270",
    "reg": "UN R150",
    "para": "Annex 7 Part 2 1.1",
    "page": 47,
    "category": "Photometric",
    "tag": "Colour & Chromaticity",
    "text": "The outer surface of the retro-reflective device and, in particular, the illuminating surface, shall be lightly wiped with a cotton cloth soaked in a detergent lubricating oil; after about 5 minutes the surface shall be cleaned and the RI shall then be measured according to paragraph 5.1.3.2.2.",
    "test": "Apply detergent lubricating oil, clean after 5 min, and measure RI at 20', 0\u00b0/0\u00b0 for compliance with Table 3."
  },
  {
    "id": "R-0271",
    "reg": "UN R10",
    "para": "3.2.6",
    "page": 6,
    "category": "Electrical/EMC",
    "tag": "Approval Marking",
    "text": "The sample(s) shall be clearly and indelibly marked with the manufacturer's trade name or mark.",
    "test": "Inspect the rear lamp ESA sample(s) for a clear, indelible manufacturer's trade name or mark."
  },
  {
    "id": "R-0272",
    "reg": "UN R10",
    "para": "3.2.6",
    "page": 6,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "The sample(s) shall be clearly and indelibly marked with the type designation.",
    "test": "Inspect the rear lamp ESA sample(s) for a clear, indelible type designation."
  },
  {
    "id": "R-0273",
    "reg": "UN R10",
    "para": "5.2.2",
    "page": 8,
    "category": "Electrical/EMC",
    "tag": "Approval Marking",
    "text": "An approval mark described in paragraph 5.3. shall be affixed to every ESA conforming to a type approved under this Regulation.",
    "test": "Inspect production rear lamps for presence of the R10 approval mark."
  },
  {
    "id": "R-0274",
    "reg": "UN R10",
    "para": "5.3.1",
    "page": 8,
    "category": "Electrical/EMC",
    "tag": "Approval Marking",
    "text": "The approval mark shall comprise a circle containing the letter \"E\", followed by the distinguishing number of the country granting the approval.",
    "test": "Inspect the approval mark for the circle with letter E and the country distinguishing number."
  },
  {
    "id": "R-0275",
    "reg": "UN R10",
    "para": "5.3.2",
    "page": 8,
    "category": "Electrical/EMC",
    "tag": "Approval Marking",
    "text": "The approval mark shall comprise the number of this Regulation, followed by the letter \"R\", a dash and the approval number to the right of the circle specified in paragraph 5.3.1.",
    "test": "Inspect the approval mark for '10R-' followed by the approval number to the right of the circle."
  },
  {
    "id": "R-0276",
    "reg": "UN R10",
    "para": "5.5",
    "page": 8,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "Markings on ESAs in conformity with paragraph 5.3. need not be visible when the ESA is installed in the vehicle.",
    "test": "Verify the mark is on the lamp (location may be hidden when installed) and matches the communication form."
  },
  {
    "id": "R-0277",
    "reg": "UN R10",
    "para": "6.1.1",
    "page": 8,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "A vehicle and its electrical/electronic system(s) or ESA(s) shall be designed, constructed and fitted in such a way as to enable the vehicle, in normal conditions of use, to comply with the requirements of this Regulation.",
    "test": "Review design and EMC test results of the rear lamp ESA demonstrating compliance with paragraph 6 requirements."
  },
  {
    "id": "R-0278",
    "reg": "UN R10",
    "para": "6.1.1.2",
    "page": 9,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "ESA(s) shall be tested for radiated and conducted emissions.",
    "test": "Confirm test report covers radiated emission (Annex 7/8) and conducted transient emission (Annex 10) tests."
  },
  {
    "id": "R-0279",
    "reg": "UN R10",
    "para": "6.1.1.2",
    "page": 9,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "ESA(s) shall be tested for immunity to radiated and conducted disturbances.",
    "test": "Confirm test report covers radiated immunity (Annex 9) and conducted transient immunity (Annex 10) tests."
  },
  {
    "id": "R-0280",
    "reg": "UN R10",
    "para": "6.5.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "The electromagnetic radiation generated by the ESA representative of its type shall be measured by the method described in Annex 7.",
    "test": "Verify broadband emission measurement was performed per Annex 7 (CISPR 25 ALSE)."
  },
  {
    "id": "R-0281",
    "reg": "UN R10",
    "para": "6.5.2.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "If measurements are made using the method described in Annex 7, the limits shall be 62 to 52 dB microvolts/m in the 30 to 75 MHz frequency band, this limit decreasing logarithmically with frequencies above 30 MHz.",
    "test": "Compare Annex 7 broadband measurements in 30\u201375 MHz against the 62\u201352 dB\u00b5V/m logarithmic limit line."
  },
  {
    "id": "R-0282",
    "reg": "UN R10",
    "para": "6.5.2.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "If measurements are made using the method described in Annex 7, the limits shall be 52 to 63 dB microvolts/m in the 75 to 400 MHz band, this limit increasing logarithmically with frequencies above 75 MHz as shown in Appendix 6.",
    "test": "Compare Annex 7 broadband measurements in 75\u2013400 MHz against the 52\u201363 dB\u00b5V/m logarithmic limit line."
  },
  {
    "id": "R-0283",
    "reg": "UN R10",
    "para": "6.5.2.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Radiated Emissions",
    "text": "In the 400 to 1,000 MHz frequency band the ESA broadband limit remains constant at 63 dB microvolts/m.",
    "test": "Compare Annex 7 broadband measurements in 400\u20131,000 MHz against 63 dB\u00b5V/m."
  },
  {
    "id": "R-0284",
    "reg": "UN R10",
    "para": "6.5.2.2",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "On the ESA representative of its type, the measured values, expressed in dB microvolts/m, shall be below the type approval limits.",
    "test": "Check all broadband readings are below the limit line across 30\u20131,000 MHz."
  },
  {
    "id": "R-0285",
    "reg": "UN R10",
    "para": "6.6.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "The electromagnetic radiation generated by the ESA representative of its type shall be measured by the method described in Annex 8.",
    "test": "Verify narrowband emission measurement was performed per Annex 8."
  },
  {
    "id": "R-0286",
    "reg": "UN R10",
    "para": "6.6.2.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "If measurements are made using the method described in Annex 8, the limits shall be 52 to 42 dB microvolts/m in the 30 to 75 MHz frequency band, this limit decreasing logarithmically with frequencies above 30 MHz.",
    "test": "Compare Annex 8 narrowband measurements in 30\u201375 MHz against the 52\u201342 dB\u00b5V/m logarithmic limit line."
  },
  {
    "id": "R-0287",
    "reg": "UN R10",
    "para": "6.6.2.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "If measurements are made using the method described in Annex 8, the limits shall be 42 to 53 dB microvolts/m in the 75 to 400 MHz band, this limit increasing logarithmically with frequencies above 75 MHz as shown in Appendix 7.",
    "test": "Compare Annex 8 narrowband measurements in 75\u2013400 MHz against the 42\u201353 dB\u00b5V/m logarithmic limit line."
  },
  {
    "id": "R-0288",
    "reg": "UN R10",
    "para": "6.6.2.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Radiated Emissions",
    "text": "In the 400 to 1,000 MHz frequency band the ESA narrowband limit remains constant at 53 dB microvolts/m.",
    "test": "Compare Annex 8 narrowband measurements in 400\u20131,000 MHz against 53 dB\u00b5V/m."
  },
  {
    "id": "R-0289",
    "reg": "UN R10",
    "para": "6.6.2.2",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "On the ESA representative of its type, the measured value, expressed in dB microvolts/m shall be below the type approval limits.",
    "test": "Check all narrowband readings are below the limit line across 30\u20131,000 MHz."
  },
  {
    "id": "R-0290",
    "reg": "UN R10",
    "para": "6.7.1",
    "page": 10,
    "category": "Electrical/EMC",
    "tag": "Transient Immunity",
    "text": "The emission of ESA representative of its type shall be tested by the method(s) according to ISO 7637-2 as described in Annex 10 for the levels given in Table 1 (maximum allowed pulse amplitude: vehicles with 12 V systems +75 V / -100 V; vehicles with 24 V systems +150 V / -450 V).",
    "test": "Measure conducted transient emissions per ISO 7637-2 and verify pulse amplitudes do not exceed Table 1 values for the applicable supply voltage."
  },
  {
    "id": "R-0291",
    "reg": "UN R10",
    "para": "6.8.1",
    "page": 11,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "The immunity to electromagnetic radiation of the ESA representative of its type shall be tested by the method(s) chosen from those described in Annex 9.",
    "test": "Verify radiated immunity testing used one or a combination of Annex 9 methods."
  },
  {
    "id": "R-0292",
    "reg": "UN R10",
    "para": "6.8.2.1",
    "page": 11,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "Test severity in over 90 per cent of the 20 to 6,000 MHz frequency band shall be as given in Table 2a.",
    "test": "Check applied test levels (e.g. ALSE 30 V/m 80\u20132,000 MHz, 10 V/m 2\u20136 GHz; BCI 60 mA) were met in over 90 % of the band."
  },
  {
    "id": "R-0293",
    "reg": "UN R10",
    "para": "6.8.2.1",
    "page": 11,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "Test severity for the minimum test level over the whole 20 to 6,000 MHz frequency band shall be as given in Table 2b.",
    "test": "Check the applied test level never fell below Table 2b minimums (e.g. ALSE 25 V/m / 8 V/m; BCI 50 mA) over the whole band."
  },
  {
    "id": "R-0294",
    "reg": "UN R10",
    "para": "6.8.2.2",
    "page": 12,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "The ESA representative of its type shall be considered as complying with immunity requirements if, during the tests performed in accordance with Annex 9, there shall be no degradation of performance of \"immunity related functions\".",
    "test": "Monitor rear position and stop lamp functions during Annex 9 exposure and confirm no incorrect operation or degradation."
  },
  {
    "id": "R-0295",
    "reg": "UN R10",
    "para": "6.9.1",
    "page": 12,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "The immunity of ESA representative of this type shall be tested by the method according to ISO 16750-2 for starting profile, as described in Annex 10, with the test levels given in Table 3a, and starting profile shall be tested according to the functional status classification as defined in ISO 16750-1.",
    "test": "Apply the ISO 16750-2 starting profile (level II, 10 pulses) and verify functional status class B for immunity related functions."
  },
  {
    "id": "R-0296",
    "reg": "UN R10",
    "para": "6.9.1",
    "page": 12,
    "category": "Electrical/EMC",
    "tag": "Transient Immunity",
    "text": "The immunity of ESA representative of this type shall be tested by the method according to ISO 7637-2 for pulses 1, 2a, 2b, 3a and 3b, as described in Annex 10, with the test levels given in Table 3b, applying the Functional Performance Status Classification (FPSC) as in ISO 7637-1.",
    "test": "Apply ISO 7637-2 pulses 1, 2a, 2b, 3a, 3b at Table 3b levels and verify FPSC (I/II/III) required for immunity related functions is achieved."
  },
  {
    "id": "R-0297",
    "reg": "UN R10",
    "para": "6.9.1",
    "page": 12,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "Starting profile is only applicable to ESAs that could be installed in vehicles with internal combustion engines which are started with a 12V/24V starter motor.",
    "test": "Determine whether the lamp may be fitted to ICE vehicles with 12/24 V starter and apply starting profile accordingly."
  },
  {
    "id": "R-0298",
    "reg": "UN R10",
    "para": "6.10.1",
    "page": 12,
    "category": "Electrical/EMC",
    "tag": "Retro-reflection",
    "text": "Where an ESA does not include an electronic oscillator with an operating frequency greater than 9 kHz, it shall be deemed to comply with paragraph 6.6.2. and with Annex 8.",
    "test": "Review LED driver schematic for oscillators > 9 kHz to determine whether the narrowband exemption applies."
  },
  {
    "id": "R-0299",
    "reg": "UN R10",
    "para": "6.10.5",
    "page": 13,
    "category": "Electrical/EMC",
    "tag": "Transient Immunity",
    "text": "ESAs that are not switched, contain no switches or do not include inductive load need not be tested for transient conducted emission and shall be deemed to comply with paragraph 6.7.",
    "test": "Review lamp circuit for switching elements or inductive loads to determine whether transient emission testing can be waived."
  },
  {
    "id": "R-0300",
    "reg": "UN R10",
    "para": "9.3.1",
    "page": 26,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "Production shall be deemed to conform in relation to broadband and narrowband electromagnetic disturbances if the levels measured do not exceed by more than 4 dB (60 per cent) the reference limits prescribed in paragraphs 6.5.2.1. and 6.6.2.1. for ESAs.",
    "test": "Measure series lamp emissions and verify they do not exceed the limits by more than 4 dB."
  },
  {
    "id": "R-0301",
    "reg": "UN R10",
    "para": "9.3.2",
    "page": 26,
    "category": "Electrical/EMC",
    "tag": "Radiated Immunity",
    "text": "Production shall be deemed to conform in relation to immunity to electromagnetic radiation if the ESA does not exhibit any degradation relating to the direct control of the vehicle which could be observed by the driver or other road user when subjected to a field strength up to 80 per cent of the reference limits prescribed in paragraph 6.8.2.1. for ESAs.",
    "test": "Expose series lamp to 80 % of paragraph 6.8.2.1 levels and confirm no observable degradation."
  },
  {
    "id": "R-0302",
    "reg": "UN R10",
    "para": "9.3.3",
    "page": 26,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "Production shall be deemed to conform in relation to immunity to conducted disturbances and emission if the component or STU shows no degradation of performance of \"immunity related functions\" up to levels given in paragraph 6.9.1. and does not exceed the levels given in paragraph 6.7.1.",
    "test": "Perform transient immunity and emission tests on series lamps and verify paragraph 6.9.1 and 6.7.1 criteria."
  },
  {
    "id": "R-0303",
    "reg": "UN R10",
    "para": "Annex 7 2.1",
    "page": 91,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "The ESA under test shall be in normal operation mode, preferably in maximum load.",
    "test": "Operate all lamp functions (position, stop, reversing) at maximum load during broadband emission test."
  },
  {
    "id": "R-0304",
    "reg": "UN R10",
    "para": "Annex 7 3.1",
    "page": 91,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "For ESA other than involved in \"REESS charging mode coupled to the power grid\" the test shall be performed according to the ALSE method described in Clause 6.4 of CISPR 25.",
    "test": "Verify test set-up follows CISPR 25 Clause 6.4 ALSE method."
  },
  {
    "id": "R-0305",
    "reg": "UN R10",
    "para": "Annex 7 4.1",
    "page": 92,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "The limits apply throughout the frequency range 30 to 1,000 MHz for measurements performed in an ALSE or OATS.",
    "test": "Confirm broadband scan covers 30\u20131,000 MHz."
  },
  {
    "id": "R-0306",
    "reg": "UN R10",
    "para": "Annex 8 3.1",
    "page": 96,
    "category": "Electrical/EMC",
    "tag": "Radiated Emissions",
    "text": "The narrowband test shall be performed according to ALSE method described in paragraph 6.4. of CISPR 25.",
    "test": "Verify test set-up follows CISPR 25 paragraph 6.4."
  },
  {
    "id": "R-0307",
    "reg": "UN R10",
    "para": "Annex 8 4.1",
    "page": 96,
    "category": "Electrical/EMC",
    "tag": "Radiated Emissions",
    "text": "The narrowband limits apply throughout the frequency range 30 to 1,000 MHz for measurements performed in an ALSE or OATS.",
    "test": "Confirm narrowband scan covers 30\u20131,000 MHz."
  },
  {
    "id": "R-0308",
    "reg": "UN R10",
    "para": "Annex 9 2.2",
    "page": 98,
    "category": "Electrical/EMC",
    "tag": "Electrical Connection",
    "text": "The ESA under test shall be switched on and shall be stimulated to be in normal operation condition.",
    "test": "Confirm lamp functions are energised and stimulated during radiated immunity testing."
  },
  {
    "id": "R-0309",
    "reg": "UN R10",
    "para": "Annex 9 3.1",
    "page": 98,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "Immunity measurements shall be made in the 20 to 6,000 MHz frequency range with frequency steps according to ISO 11452-1.",
    "test": "Verify immunity test frequency range 20\u20136,000 MHz and ISO 11452-1 step sizes."
  },
  {
    "id": "R-0310",
    "reg": "UN R10",
    "para": "Annex 9 3.1",
    "page": 98,
    "category": "Electrical/EMC",
    "tag": "Electrical/EMC Provision",
    "text": "The test signal modulation shall be AM (amplitude modulation), with 1 kHz modulation and 80 per cent modulation depth in the 20 to 400 MHz frequency range.",
    "test": "Check generator settings: AM 1 kHz, 80 % depth for 20\u2013400 MHz."
  },
  {
    "id": "R-0311",
    "reg": "UN R10",
    "para": "Annex 9 3.1",
    "page": 98,
    "category": "Electrical/EMC",
    "tag": "Transient Immunity",
    "text": "The test signal modulation shall be PM2 (pulse modulation type 2), Ton 3 \u00b5s, period 3,333 \u00b5s in the 2,700 to 3,100 MHz frequency range.",
    "test": "Check generator settings: PM2, Ton 3 \u00b5s, period 3,333 \u00b5s for 2,700\u20133,100 MHz."
  },
  {
    "id": "R-0312",
    "reg": "UN R10",
    "para": "Annex 9 3.1",
    "page": 98,
    "category": "Electrical/EMC",
    "tag": "Transient Immunity",
    "text": "The test signal modulation shall be PM3 (pulse modulation type 3), Ton 500 \u00b5s, period 1,000 \u00b5s in the 380 to 2,700 MHz and the 3,100 to 6,000 MHz frequency ranges.",
    "test": "Check generator settings: PM3, Ton 500 \u00b5s, period 1,000 \u00b5s for 380\u20132,700 MHz and 3,100\u20136,000 MHz."
  },
  {
    "id": "R-0313",
    "reg": "UN R10",
    "para": "Annex 10 2",
    "page": 108,
    "category": "Electrical/EMC",
    "tag": "Transient Immunity",
    "text": "Test pulses 1, 2a, 2b, 3a and 3b according to ISO 7637-2 and the starting profile according to ISO 16750-2 shall be applied to the supply lines as well as to other connections of ESAs which may be operationally connected to supply lines.",
    "test": "Verify transient immunity pulses were applied to lamp supply lines and any connections operationally connected to supply."
  },
  {
    "id": "R-0314",
    "reg": "UN R10",
    "para": "Annex 10 3",
    "page": 108,
    "category": "Electrical/EMC",
    "tag": "Colour & Chromaticity",
    "text": "Emission of transient conducted disturbances shall be measured according to ISO 7637-2 on supply lines as well as other connections of ESAs which may be operationally connected to supply lines.",
    "test": "Verify transient emission measurement was made on supply lines and operationally connected lines."
  }
];

const bumper: Obligation[] = [
  { id: "B-0004", reg: "UN R48", para: "6.14.4", page: 88, category: "Installation & Visibility", tag: "Retro-reflector Height", text: "Rear retro-reflectors integrated in the bumper shall be mounted not less than 250 mm and not more than 900 mm above the ground.", test: "On-vehicle height measurement at unladen mass." },
  { id: "B-0011", reg: "UN R150", para: "6.1.2", page: 11, category: "Photometric", tag: "Retro-reflection", text: "Class IA retro-reflectors shall meet the minimum CIL values of Annex 6.", test: "CIL measurement at prescribed observation/entrance angles." },
  { id: "B-0019", reg: "UN R10", para: "6.8.2", page: 22, category: "Electrical/EMC", tag: "Conducted Transients", text: "Bumper-mounted parking sensor ESAs shall be immune to ISO 7637-2 pulses 1, 2a, 3a, 3b and 4.", test: "ISO 7637-2 bench test, functional class A for pulses 3a/3b." },
  { id: "B-0026", reg: "UN R148", para: "7.1", page: 31, category: "COP", tag: "Conformity of Production", text: "Integrated lamps shall not deviate unfavourably by more than 20% from prescribed values in production.", test: "Random sampling, photometric check." },
];

export const CASES = {
  "dev-rear-lamp": { label: "Worked Example: dev-rear-lamp (Rear Lamp)", component: "Rear Lamp", obligations: rearLamp },
  "heldout-front-bumper": { label: "Sunday Held-out: heldout-front-bumper (Front Bumper)", component: "Front Bumper", obligations: bumper },
} as const;

export type CaseId = keyof typeof CASES;

export const PRUNED = [
  { para: "UN R148 §5.9", reason: "Applies to rear fog lamps — not part of this component" },
  { para: "UN R148 §5.11", reason: "Reversing lamp requirements — separate device" },
  { para: "UN R48 §6.2", reason: "Dipped-beam headlamp installation — front lighting only" },
  { para: "UN R150 §6.8", reason: "Conspicuity marking for N3/O4 vehicles — M1 out of scope" },
  { para: "UN R10 §6.9", reason: "RESS charging-mode emissions — not applicable to 12V lamp" },
  { para: "UN R48 §6.21", reason: "Contour marking — category M1 exempt" },
  { para: "UN R48 §6.1", reason: "Main-beam headlamp installation — not applicable" },
  { para: "UN R48 §6.3", reason: "Front fog lamp installation — front lighting only" },
  { para: "UN R48 §6.4", reason: "Reversing lamp installation — separate component" },
  { para: "UN R48 §6.5", reason: "Direction indicator lamp — separate function" },
  { para: "UN R48 §6.6", reason: "Hazard warning signal — system level switch requirement" },
  { para: "UN R48 §6.8", reason: "Rear registration plate illuminating device — separate lamp" },
  { para: "UN R48 §6.9", reason: "Front position lamp — front lighting only" },
  { para: "UN R48 §6.11", reason: "Rear fog lamp — separate lamp assembly" },
  { para: "UN R48 §6.12", reason: "Parking lamp — out of scope for fixed body rear combination" },
  { para: "UN R48 §6.13", reason: "End-outline marker lamp — category M1 exempt" },
  { para: "UN R48 §6.15", reason: "Side retro-reflector, non-triangular — side body only" },
  { para: "UN R48 §6.16", reason: "Rear retro-reflector, triangular — trailer only" },
  { para: "UN R48 §6.17", reason: "Front retro-reflector, non-triangular — front body only" },
  { para: "UN R48 §6.18", reason: "Side marker lamps — commercial vehicle / length > 6m only" },
  { para: "UN R48 §6.19", reason: "Daytime running lamp — front lighting only" },
  { para: "UN R48 §6.20", reason: "Cornering lamp — front lighting only" },
  { para: "UN R48 §6.22", reason: "Adaptive front-lighting system (AFS) — front lighting only" },
  { para: "UN R48 §6.24", reason: "Exterior courtesy lamp — door/mirror mounted only" },
  { para: "UN R48 §6.25", reason: "Rear-end collision alert signal — active ADAS function only" },
  { para: "UN R48 §6.26", reason: "Manoeuvring lamp — specialized utility lighting only" },
];

export const DIFF = {
  modified: [
  {
    "para": "\u00a75.1.2",
    "old": "Prior revision wording (superseded)",
    "new": "An accelerator control application resulting in continuous acceleration and having a velocity of at least 400 per cent per second over a travel distance of at least 70 per cent of the total travel distance of the accelerator control, and reaching a maximum position of the accelerator control of at least 90 per cent with that velocity shall be regarded as an accelerator control misapplication in the context of the paragraph 5.1.1.",
    "reason": "Paragraph 5.1.2 of UN R175 was amended in version 1.0.0: 'The accelerator control application having a velocity' became 'An accelerator control application resulting in continuous acceleration and having a velocity'."
  },
  {
    "para": "\u00a75.1.4",
    "old": "Prior revision wording (superseded)",
    "new": "The ACPE shall control acceleration when the vehicle is accelerated both from standstill and, as relevant, while creeping.",
    "reason": "Paragraph 5.1.4 of UN R175 was amended in version 1.0.0: 'When the vehicle is accelerated from standstill' became 'when the vehicle is accelerated both from standstill and, as relevant, while creeping'."
  },
  {
    "para": "\u00a75.1.5",
    "old": "Prior revision wording (superseded)",
    "new": "The ACPE shall limit vehicle acceleration in order to prevent or mitigate a collision with an obstacle located not more than 1.5 m in front of or behind the vehicle, in the vehicle path, at the time the triggering conditions (as outlined in paragraph 5.1.2.) are achieved, provided: (a) the road is flat, horizontal and dry affording good adhesion and the weather conditions do not affect the performance of the vehicle; (b) the tyres are in an appropriate state and properly inflated; the brakes if intended to be used are properly operational; there is no severe uneven load distribution; no trailer is coupled and the mass is between maximum mass and mass in running order; the powertrain management system is properly operational; if equipped, rear hatches, trunk lids or tailgates are closed and latched; (c) ambient illumination is at least 1000 Lux with no extreme blinding of the sensors; the target vehicle is not extreme with regard to RCS or shape/silhouette; no significant weather conditions affect sensing; no overhead obstructions close to the vehicle; (d) the obstacle is stationary, unobstructed, clearly separated from other objects in the driving direction; for a vehicle obstacle, its centre line is located between two vertical longitudinal planes defining the extreme outer edge of the vehicle; for a wall obstacle, the overlap between wall and vehicle is at least 1.0 m; for a pedestrian obstacle, the distance between its centre line and the vehicle centre line is not more than 25 per cent of the vehicle width; the direction of travel is straight with no curve, not turning at an intersection and following its lane; the obstacle is an M1 vehicle, a wall-like structure at least 2.0 m wide and 1.0 m high, or a pedestrian silhouette relating to a human being; the obstacle is at least 1.0m from the vehicle when the triggering conditions are achieved; the vehicle is at or below its maximum creeping speed forward and at or below 4km/h rearward.",
    "reason": "Paragraph 5.1.5 of UN R175 was amended in version 1.0.0: 'located between 1.0 m and 1.5 m' became 'located not more than 1.5 m ... at the time the triggering conditions (as outlined in paragraph 5.1.2.) are achieved'; 'The lateral offset ... is not more than 0.2 m' was replaced by vehicle, wall and pedestrian obstacle positioning conditions; conditions on closed tailgates, obstacle type, minimum 1.0m distance and creeping/4km/h speed were added."
  },
  {
    "para": "\u00a76.5.2",
    "old": "Prior revision wording (superseded)",
    "new": "The lateral offset between the centreline of the vehicle target and the centreline of the vehicle shall be between 0.0 m and the distance to extreme outer edge of the vehicle.",
    "reason": "Paragraph 6.5.2 (formerly 6.5) of UN R175 was amended in version 1.0.0: 'between 0.0 m and 0.2 m' became 'between 0.0 m and the distance to extreme outer edge of the vehicle'."
  },
  {
    "para": "\u00a76.6",
    "old": "Prior revision wording (superseded)",
    "new": "The test procedures shall be performed both in a forward and rearward direction and at least with the ACPE interventions triggered at 1.0 m (+0.1 m tolerance) and 1.5 m (-0.1 m tolerance) distance from the target position (as detailed in Table 1).",
    "reason": "Paragraph 6.6 (formerly 6.5) of UN R175 was amended in version 1.0.0: 'with the vehicle situated 1.0 m ... and 1.5 m ... from the target position at the start of the test' became 'with the ACPE interventions triggered at 1.0 m ... and 1.5 m ... distance from the target position'; 'with and without an expected ACPE intervention' was removed."
  },
  {
    "para": "\u00a76.6.1.2",
    "old": "Prior revision wording (superseded)",
    "new": "The procedure for each test with a stationary (non-creeping) vehicle shall be as follows: (a) Position the vehicle at a distance to the relevant target or speed measurement point as defined in Table 1.",
    "reason": "Paragraph 6.6.1.2 (formerly 6.5) of UN R175 was amended in version 1.0.0: 'each accelerator control misapplication test' became 'each test with a stationary (non-creeping) vehicle' and 'to the target' became 'to the relevant target'."
  }
],
  added: [
  {
    "para": "\u00a75.1.4.1",
    "text": "An ACPE intervention is not required when: (a) there is an AEBS warning or intervention occurring; or (b) the vehicle speed is greater than 10 km/h.",
    "reason": "Paragraph 5.1.4.1 of UN R175 is new in version 1.0.0: 'An ACPE intervention is not required when: (a) there is an AEBS warning or intervention occurring...'."
  },
  {
    "para": "\u00a75.1.6.2",
    "text": "When a collision is not prevented during acceleration while creeping, the ACPE shall reduce the effective demand of the accelerator control to zero at or before the point of collision.",
    "reason": "Paragraph 5.1.6.2 of UN R175 is new in version 1.0.0: 'Acceleration while creeping, In the case a collision is not prevented, the ACPE shall reduce the effective demand...'."
  },
  {
    "para": "\u00a76.4.2",
    "text": "The targets used for the pedestrian detection tests shall be a child articulated 'soft target' in its resting position with the articulation switched off, representative of the human attributes applicable to the sensor system of the ACPE under test according to ISO 19206-2:2018.",
    "reason": "Paragraph 6.4.2 of UN R175 is new in version 1.0.0: 'The targets used for the pedestrian detection tests shall be a child articulated \"soft target\"...'."
  },
  {
    "para": "\u00a76.5.1",
    "text": "The reference point for the location of the vehicle shall be the most rearward point on the centreline of the vehicle when going rearwards, and the most forward point of the vehicle when going forwards.",
    "reason": "Paragraph 6.5.1 of UN R175 is new in version 1.0.0: 'The reference point for the location of the vehicle shall be the most rearward point on the centreline...'."
  },
  {
    "para": "\u00a76.5.3",
    "text": "The lateral offset between the centre line of the pedestrian obstacle and the centre line of the vehicle shall be not more than 25 per cent of the vehicle width.",
    "reason": "Paragraph 6.5.3 of UN R175 is new in version 1.0.0: 'The lateral offset between the centre line of the pedestrian obstacle and the centre line of the vehicle...'."
  },
  {
    "para": "\u00a76.5.5",
    "text": "The orientation of the vehicle target shall be 0\u00b0 or 180\u00b0 as defined in ISO 19206-3:2021, chosen by the Technical Service.",
    "reason": "Paragraph 6.5.5 of UN R175 is new in version 1.0.0: 'The orientation of the vehicle target shall be 0\u00b0 or 180\u00b0 respectively as defined in ISO 19206-3:2021...'."
  },
  {
    "para": "\u00a76.6.1.1",
    "text": "Each test condition according to Table 1 (forward and rearward driving directions at 1.0 m (+0.1 m) and 1.5 m (-0.1 m) distance to target) shall be tested with a stationary vehicle both with and without the presence of the target.",
    "reason": "Paragraph 6.6.1.1 of UN R175 is new in version 1.0.0: 'Each test condition according to Table 1 shall be tested with and without the presence of the target...'."
  },
  {
    "para": "\u00a76.6.1.1",
    "text": "For stationary vehicle tests without a target, the ACPE shall be deactivated if necessary.",
    "reason": "Paragraph 6.6.1.1 of UN R175 is new in version 1.0.0: 'Each test condition according to Table 1 shall be tested with and without the presence of the target. For tests without a target the ACPE shall be deactivated if necessary...'."
  },
  {
    "para": "\u00a76.6.1.1",
    "text": "Stationary vehicle tests without a target may be combined where feasible.",
    "reason": "Paragraph 6.6.1.1 of UN R175 is new in version 1.0.0: 'Each test condition according to Table 1 shall be tested with and without the presence of the target. For tests without a target ... may be combined where feasible...'."
  },
  {
    "para": "\u00a76.6.2.1",
    "text": "Each test condition according to Table 1 shall be tested once with a creeping vehicle, with a starting point and a profile of the accelerator control application selected at the discretion of the Technical Service.",
    "reason": "Paragraph 6.6.2.1 of UN R175 is new in version 1.0.0: 'Each test condition according to Table 1 shall be tested once with a starting point and a profile of the accelerator control application selected at the discretion of the Technical Service...'."
  },
  {
    "para": "\u00a76.6.2.1",
    "text": "For creeping vehicle tests in the forward direction, the starting point and the accelerator control application profile shall be selected such that the triggering condition (paragraph 5.1.2.) is achieved as close to the maximum creeping speed as reasonably practical whilst remaining at or below that speed and avoiding any AEBS warning or intervention which results in an ACPE intervention not occurring.",
    "reason": "Paragraph 6.6.2.1 of UN R175 is new in version 1.0.0: 'Each test condition according to Table 1 shall be tested once with a starting point and a profile of the accelerator control application selected at the discretion of the Technical Service...'."
  },
  {
    "para": "\u00a76.6.2.1",
    "text": "For creeping vehicle tests in the rearward direction, the starting point and the accelerator control application profile shall be selected such that the triggering condition (paragraph 5.1.2.) is achieved as close to 4 km/h as reasonably practical whilst remaining at or below that speed and avoiding any AEBS warning or intervention which results in an ACPE intervention not occurring.",
    "reason": "Paragraph 6.6.2.1 of UN R175 is new in version 1.0.0: 'Each test condition according to Table 1 shall be tested once with a starting point and a profile of the accelerator control application selected at the discretion of the Technical Service...'."
  },
  {
    "para": "\u00a76.6.2.2",
    "text": "The procedure for each test with a creeping vehicle shall be to position the vehicle at the selected starting point as determined by paragraph 6.6.2.1.",
    "reason": "Paragraph 6.6.2.2 of UN R175 is new in version 1.0.0: 'The procedure for each test with a creeping vehicle shall be as follows: (a) Position the vehicle at the selected starting point...'."
  },
  {
    "para": "\u00a76.6.2.2",
    "text": "The procedure for each test with a creeping vehicle shall be to hold the vehicle stationary and select the corresponding driving direction.",
    "reason": "Paragraph 6.6.2.2 of UN R175 is new in version 1.0.0: 'The procedure for each test with a creeping vehicle shall be as follows: ... (b) Hold the vehicle stationary and select the corresponding driving direction...'."
  },
  {
    "para": "\u00a76.6.2.2",
    "text": "The procedure for each test with a creeping vehicle shall be to release the braking system so that the vehicle starts creeping.",
    "reason": "Paragraph 6.6.2.2 of UN R175 is new in version 1.0.0: 'The procedure for each test with a creeping vehicle shall be as follows: ... (c) Release the braking system so that the vehicle starts creeping...'."
  },
  {
    "para": "\u00a76.6.2.2",
    "text": "The procedure for each test with a creeping vehicle shall be to operate the accelerator control in order to achieve the relevant triggering conditions (paragraph 5.1.2.) at the point the vehicle has reached the distance to target according to Table 1.",
    "reason": "Paragraph 6.6.2.2 of UN R175 is new in version 1.0.0: 'The procedure for each test with a creeping vehicle shall be as follows: ... (d) Operate the accelerator control in order to achieve the relevant triggering conditions...'."
  },
  {
    "para": "\u00a76.6.2.2",
    "text": "When a collision is not prevented during the procedure for each test with a creeping vehicle, the manufacturer shall demonstrate to the satisfaction of the Technical Service that the intervention complies with the requirements of paragraph 5.1.6.2.",
    "reason": "Paragraph 6.6.2.2 of UN R175 is new in version 1.0.0: 'The procedure for each test with a creeping vehicle shall be as follows: ... (e) In the case a collision is not prevented the manufacturer shall demonstrate...'."
  }
],
  removed: [
  {
    "para": "\u00a7",
    "text": "Provisions repealed in revised regulation.",
    "reason": "Paragraph 6.5 of UN R175 was amended in version 1.0.0; the provision 'the vehicle shall be allowed to be driven in the direction of the target for a distance of up to 20 m to the start position and/or the engine shall be allowed to be switched \"off\" and \"on\"' no longer appears."
  }
],
};
