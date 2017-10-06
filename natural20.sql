--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: attacks; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE attacks (
    attack_id integer NOT NULL,
    monster_id integer NOT NULL,
    name character varying(24) NOT NULL,
    damage_type character varying(24),
    avg_damage integer NOT NULL,
    num_dice integer,
    type_dice integer,
    dice_modifier integer
);


ALTER TABLE attacks OWNER TO sarah;

--
-- Name: attacks_attack_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE attacks_attack_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE attacks_attack_id_seq OWNER TO sarah;

--
-- Name: attacks_attack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE attacks_attack_id_seq OWNED BY attacks.attack_id;


--
-- Name: friendships; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE friendships (
    friendship_id integer NOT NULL,
    user_id_1 integer NOT NULL,
    user_id_2 integer NOT NULL,
    verified boolean NOT NULL
);


ALTER TABLE friendships OWNER TO sarah;

--
-- Name: friendships_friendship_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE friendships_friendship_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE friendships_friendship_id_seq OWNER TO sarah;

--
-- Name: friendships_friendship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE friendships_friendship_id_seq OWNED BY friendships.friendship_id;


--
-- Name: goals; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE goals (
    goal_id integer NOT NULL,
    user_id integer NOT NULL,
    goal_type character varying(20) NOT NULL,
    valid_from timestamp without time zone NOT NULL,
    valid_to timestamp without time zone,
    value integer NOT NULL,
    xp integer NOT NULL,
    frequency character varying(7),
    resolved character varying(1)
);


ALTER TABLE goals OWNER TO sarah;

--
-- Name: goals_goal_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE goals_goal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE goals_goal_id_seq OWNER TO sarah;

--
-- Name: goals_goal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE goals_goal_id_seq OWNED BY goals.goal_id;


--
-- Name: goalstatuses; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE goalstatuses (
    goalstatus_id integer NOT NULL,
    goal_id integer NOT NULL,
    date_recorded timestamp without time zone NOT NULL,
    value integer NOT NULL
);


ALTER TABLE goalstatuses OWNER TO sarah;

--
-- Name: goalstatuses_goalstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE goalstatuses_goalstatus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE goalstatuses_goalstatus_id_seq OWNER TO sarah;

--
-- Name: goalstatuses_goalstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE goalstatuses_goalstatus_id_seq OWNED BY goalstatuses.goalstatus_id;


--
-- Name: levellookup; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE levellookup (
    level integer NOT NULL,
    min_cr double precision,
    max_cr double precision,
    required_xp integer,
    hit_point_max integer
);


ALTER TABLE levellookup OWNER TO sarah;

--
-- Name: levellookup_level_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE levellookup_level_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE levellookup_level_seq OWNER TO sarah;

--
-- Name: levellookup_level_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE levellookup_level_seq OWNED BY levellookup.level;


--
-- Name: monsters; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE monsters (
    monster_id integer NOT NULL,
    name character varying(32) NOT NULL,
    cr double precision NOT NULL
);


ALTER TABLE monsters OWNER TO sarah;

--
-- Name: monsters_monster_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE monsters_monster_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE monsters_monster_id_seq OWNER TO sarah;

--
-- Name: monsters_monster_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE monsters_monster_id_seq OWNED BY monsters.monster_id;


--
-- Name: sleepstatuses; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE sleepstatuses (
    goalstatus_id integer NOT NULL,
    bedtime timestamp without time zone NOT NULL,
    waketime timestamp without time zone NOT NULL
);


ALTER TABLE sleepstatuses OWNER TO sarah;

--
-- Name: teams; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE teams (
    team_id integer NOT NULL,
    teamname character varying(32) NOT NULL
);


ALTER TABLE teams OWNER TO sarah;

--
-- Name: teams_team_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE teams_team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teams_team_id_seq OWNER TO sarah;

--
-- Name: teams_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE teams_team_id_seq OWNED BY teams.team_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(12) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(32) NOT NULL
);


ALTER TABLE users OWNER TO sarah;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO sarah;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: userstatuses; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE userstatuses (
    userstatus_id integer NOT NULL,
    user_id integer NOT NULL,
    level integer NOT NULL,
    current_xp integer NOT NULL,
    current_hp integer NOT NULL,
    date_recorded timestamp without time zone NOT NULL
);


ALTER TABLE userstatuses OWNER TO sarah;

--
-- Name: userstatuses_userstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE userstatuses_userstatus_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE userstatuses_userstatus_id_seq OWNER TO sarah;

--
-- Name: userstatuses_userstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE userstatuses_userstatus_id_seq OWNED BY userstatuses.userstatus_id;


--
-- Name: userteams; Type: TABLE; Schema: public; Owner: sarah; Tablespace: 
--

CREATE TABLE userteams (
    userteam_id integer NOT NULL,
    team_id integer NOT NULL,
    user_id integer NOT NULL,
    valid_from timestamp without time zone NOT NULL,
    valid_to timestamp without time zone
);


ALTER TABLE userteams OWNER TO sarah;

--
-- Name: userteams_userteam_id_seq; Type: SEQUENCE; Schema: public; Owner: sarah
--

CREATE SEQUENCE userteams_userteam_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE userteams_userteam_id_seq OWNER TO sarah;

--
-- Name: userteams_userteam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sarah
--

ALTER SEQUENCE userteams_userteam_id_seq OWNED BY userteams.userteam_id;


--
-- Name: attack_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY attacks ALTER COLUMN attack_id SET DEFAULT nextval('attacks_attack_id_seq'::regclass);


--
-- Name: friendship_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY friendships ALTER COLUMN friendship_id SET DEFAULT nextval('friendships_friendship_id_seq'::regclass);


--
-- Name: goal_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY goals ALTER COLUMN goal_id SET DEFAULT nextval('goals_goal_id_seq'::regclass);


--
-- Name: goalstatus_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY goalstatuses ALTER COLUMN goalstatus_id SET DEFAULT nextval('goalstatuses_goalstatus_id_seq'::regclass);


--
-- Name: level; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY levellookup ALTER COLUMN level SET DEFAULT nextval('levellookup_level_seq'::regclass);


--
-- Name: monster_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY monsters ALTER COLUMN monster_id SET DEFAULT nextval('monsters_monster_id_seq'::regclass);


--
-- Name: team_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY teams ALTER COLUMN team_id SET DEFAULT nextval('teams_team_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: userstatus_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY userstatuses ALTER COLUMN userstatus_id SET DEFAULT nextval('userstatuses_userstatus_id_seq'::regclass);


--
-- Name: userteam_id; Type: DEFAULT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY userteams ALTER COLUMN userteam_id SET DEFAULT nextval('userteams_userteam_id_seq'::regclass);


--
-- Data for Name: attacks; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY attacks (attack_id, monster_id, name, damage_type, avg_damage, num_dice, type_dice, dice_modifier) FROM stdin;
1	0	Dagger	piercing	4	1	4	4
2	0	Sling	bludgeoning	4	1	4	4
3	1	Spear	piercing	3	1	6	4
4	2	Blood	piercing	5	1	4	4
5	3	Talon	slashing	4	1	4	4
6	3	Javelin	piercing	5	1	6	6
7	4	Bite	bludgeoning	3	1	4	4
8	4	Spear	piercing	4	1	6	6
9	5	Bite	piercing	3	1	6	6
10	5	Claws	slashing	5	2	4	6
11	6	Shortsword	piercing	5	1	6	6
12	6	Hand	piercing	5	1	6	6
13	7	Longsword	slashing	5	1	8	8
14	8	Scimitar	slashing	5	1	6	6
15	8	Shortbow	piercing	5	1	6	6
16	9	Spiked	bludgeoning	5	1	4	4
17	10	Bite	piercing	4	1	4	4
18	10	Sting	piercing	4	1	4	4
19	11	Bite	piercing	6	2	4	4
20	12	Shortsword	piercing	5	1	6	6
21	12	Shortbow	piercing	5	1	6	6
22	13	Longsword	slashing	1	1	6	6
23	13	Shortbow	piercing	1	1	6	6
24	14	Claws	slashing	2	1	4	6
25	15	Rotting	necrotic	4	1	8	6
26	16	Slam	bludgeoning	4	1	6	6
27	17	Bite	piercing	3	1	4	4
28	18	Crush	bludgeoning	6	1	6	6
29	19	Claws	slashing	4	1	4	4
30	20	Bite	piercing	4	1	4	4
31	20	Spear	piercing	5	1	6	6
32	20	Longbow	piercing	5	1	8	8
33	21	War	piercing	6	1	8	8
34	21	Poisoned	piercing	4	1	4	4
35	22	Pseudopod	bludgeoning	4	1	6	6
36	23	Longsword	slashing	5	1	8	8
37	23	Longbow	piercing	5	1	8	8
38	24	Claws	slashing	3	1	4	4
39	25	Bite	piercing	5	1	6	6
40	25	Heavy	bludgeoning	5	1	6	6
41	25	Javelin	piercing	5	1	6	6
42	25	Spiked	piercing	5	1	6	6
43	26	Claws	slashing	3	1	4	4
44	27	Touch	fire	7	2	6	4
45	28	Greataxe	slashing	9	1	12	12
46	28	Javelin	piercing	6	1	6	6
47	29	Bite	piercing	5	1	8	8
48	30	Bite	piercing	3	1	4	4
49	30	Claws	slashing	3	1	4	4
50	30	Spear	piercing	4	1	6	6
51	31	Ram	bludgeoning	6	2	4	4
52	31	Shortsword	piercing	6	1	6	6
53	31	Shortbow	piercing	6	1	6	6
54	32	Strength	necrotic	9	2	6	6
55	33	Hooves	bludgeoning	11	2	6	6
56	34	Slam	bludgeoning	5	1	6	6
57	35	Bite	piercing	7	1	10	10
58	36	Morningstar	piercing	11	2	8	8
59	36	Javelin	piercing	9	2	6	6
60	37	Bite	piercing	7	1	10	10
61	38	Club	bludgeoning	2	1	4	10
62	39	War	piercing	6	1	8	8
63	39	Javelin	piercing	5	1	6	6
64	40	Bite	piercing	9	2	6	6
65	40	Claws	slashing	7	2	4	4
66	41	Claws	slashing	6	2	4	4
67	41	Club	bludgeoning	3	1	4	4
68	42	Beak	piercing	8	1	10	10
69	42	Claws	slashing	10	2	6	6
70	43	Sting	piercing	5	1	4	4
71	44	Claws	piercing	5	1	4	4
72	46	Bite	piercing	15	2	10	10
73	46	Claw	slashing	8	1	8	8
74	47	Bite	slashing	10	2	6	6
75	48	Warhammer	bludgeoning	7	1	8	8
76	49	Bite	piercing	7	1	10	10
77	50	Bite	piercing	8	1	10	10
78	51	Pike	piercing	9	1	10	10
79	51	Hooves	bludgeoning	11	2	6	6
80	51	Longbow	piercing	6	1	8	8
81	52	Bite	piercing	6	1	8	8
82	52	Claws	slashing	7	2	4	4
83	53	Bite	piercing	5	1	6	6
84	53	Claws	slashing	5	1	6	6
85	54	Pseudopod	acid	10	3	6	6
86	55	Bite	piercing	12	2	8	8
87	55	Claws	slashing	10	2	6	6
88	56	Bites	piercing	17	5	6	6
89	57	Bite	piercing	7	1	10	10
90	58	Tentacles	slashing	9	2	6	6
91	58	Beak	piercing	5	1	6	6
92	59	Beak	piercing	8	1	8	8
93	59	Claws	slashing	11	2	6	6
94	60	Bite	piercing	8	1	8	8
95	60	Claws	slashing	9	2	4	4
96	60	Harpoon	piercing	11	2	6	6
97	61	Pseudopod	bludgeoning	7	1	8	8
98	61	Bite	piercing	7	1	8	8
99	62	Greataxe	slashing	17	2	12	12
100	62	Gore	piercing	13	2	8	8
101	63	Pseudopod	bludgeoning	9	2	6	6
102	64	Greatclub	bludgeoning	13	2	8	8
103	64	Javelin	piercing	11	2	6	6
104	65	Morningstar	piercing	13	2	8	8
105	66	Hooves	bludgeoning	11	2	6	6
106	67	Bite	piercing	14	3	6	6
107	69	Claws	slashing	10	2	6	6
108	70	Bite	piercing	9	1	10	10
109	71	Bite	piercing	4	1	4	4
110	71	Shortsword	piercing	5	1	6	6
111	71	Hand	piercing	5	1	6	6
112	72	Bite	piercing	7	1	10	10
113	74	Tail	bludgeoning	18	4	6	6
114	75	Bite	piercing	10	2	6	6
115	76	Beard	piercing	6	1	8	8
116	76	Glaive	slashing	8	1	10	10
117	77	Bite	piercing	8	1	10	10
118	78	Slam	bludgeoning	7	1	6	6
119	79	Bite	piercing	9	1	10	10
120	80	Claws	slashing	13	2	8	8
121	81	Bite	piercing	7	1	8	8
122	82	Bite	piercing	7	1	8	8
123	82	Claw	slashing	6	1	6	6
124	82	Tail	piercing	7	1	8	8
125	83	Greataxe	slashing	17	2	12	12
126	83	Gore	piercing	13	2	8	8
127	84	Rotting	bludgeoning	10	2	6	6
128	85	Hooves	bludgeoning	13	2	8	8
129	86	Beak	piercing	10	1	10	10
130	86	Claws	slashing	14	2	8	8
131	87	Bite	piercing	6	1	8	8
132	87	Claws	slashing	7	2	4	4
133	87	Spear	piercing	5	1	6	6
134	88	Life	necrotic	5	1	6	6
135	88	Longsword	slashing	6	1	8	8
136	88	Longbow	piercing	6	1	8	8
137	89	Pseudopod	bludgeoning	6	1	6	6
138	90	Pincer	bludgeoning	11	2	6	6
139	91	Bite	piercing	8	1	6	6
140	91	Constrict	bludgeoning	10	2	6	6
141	92	Battleaxe	slashing	14	2	8	8
142	92	Morningstar	piercing	14	2	8	8
143	93	Withering	necrotic	17	4	6	6
144	94	Claws	slashing	14	2	10	10
145	94	Dagger	piercing	5	1	4	4
146	95	Bite	piercing	9	1	10	10
147	96	Claw	slashing	6	1	6	6
148	97	Maul	bludgeoning	10	2	6	6
149	97	Tusks	slashing	10	2	6	6
150	98	Bite	piercing	8	1	10	10
151	98	Claw	slashing	7	1	8	8
152	98	Scimitar	slashing	6	1	6	6
153	98	Longbow	piercing	6	1	8	8
154	99	Slam	bludgeoning	14	2	8	8
155	100	Claw	piercing	6	1	6	6
156	100	Tail	piercing	10	2	6	6
157	101	Bite	piercing	30	4	12	12
158	102	Slam	bludgeoning	14	2	8	8
159	103	Touch	fire	10	2	6	6
160	104	Slam	bludgeoning	13	2	8	8
161	105	Gore	piercing	18	2	12	12
162	105	Hooves	bludgeoning	16	2	10	10
163	106	Longsword	slashing	7	1	8	8
164	106	Shortsword	piercing	6	1	6	6
165	106	Heavy	piercing	6	1	10	10
166	107	Greatclub	bludgeoning	18	3	8	8
167	107	Rock	bludgeoning	21	3	10	10
168	108	Claws	slashing	13	2	8	8
169	109	Bite	piercing	12	2	8	8
170	109	Tentacle	bludgeoning	7	1	8	8
171	110	Bite	piercing	22	4	8	8
172	111	Spear	piercing	11	2	6	6
173	111	Tail	bludgeoning	11	2	6	6
174	112	Slam	bludgeoning	13	2	8	8
175	113	Gore	piercing	24	4	8	8
176	113	Stomp	bludgeoning	22	3	10	10
177	114	Bite	piercing	7	1	6	6
178	114	Claws	slashing	11	2	6	6
179	115	Hooves	bludgeoning	11	2	6	6
180	115	Horn	piercing	8	1	8	8
181	116	Claws	slashing	8	2	4	4
182	116	Bite	piercing	6	1	6	6
183	117	Slam	bludgeoning	13	2	8	8
184	118	Bite	piercing	15	2	10	10
185	118	Claw	slashing	13	2	8	8
186	118	Greataxe	slashing	10	1	12	12
187	119	Life	necrotic	21	4	8	8
188	120	Claw	slashing	6	1	6	6
189	120	Bite	piercing	13	3	6	6
190	121	Bite	piercing	11	2	6	6
191	121	Horns	bludgeoning	10	1	12	12
192	121	Claws	slashing	11	2	6	6
193	122	Bite	piercing	2	1	4	6
194	122	Longsword	slashing	7	1	8	8
195	122	Longbow	piercing	7	1	8	8
196	123	Slam	bludgeoning	10	2	6	6
197	124	Snake	piercing	4	1	4	4
198	124	Shortsword	piercing	5	1	6	6
199	124	Longbow	piercing	6	1	8	8
200	125	Beak	piercing	10	2	6	6
201	125	Talons	slashing	14	2	10	10
202	126	Bite	piercing	11	2	6	6
203	126	Claws	slashing	13	2	8	8
204	126	Sting	piercing	11	2	6	6
205	127	Bite	piercing	15	2	10	10
206	127	Claw	slashing	11	2	6	6
207	128	Bite	piercing	15	2	10	10
208	128	Claw	slashing	11	2	6	6
209	129	Claw	slashing	8	1	8	8
210	129	Glaive	slashing	15	2	10	10
211	130	Fist	bludgeoning	11	2	6	6
212	131	Greatclub	bludgeoning	19	3	8	8
213	131	Rock	bludgeoning	28	4	10	10
214	132	Bite	piercing	15	2	10	10
215	132	Claw	slashing	11	2	6	6
216	133	Bite	piercing	15	2	10	10
217	133	Claw	slashing	11	2	6	6
218	134	Chain	slashing	11	2	6	6
219	135	Bite	piercing	10	2	6	6
220	135	Tail	slashing	7	1	8	8
221	136	Greataxe	slashing	25	3	12	12
222	136	Rock	bludgeoning	28	4	10	10
223	137	Bite	piercing	15	2	10	10
224	137	Claw	slashing	11	2	6	6
225	138	Bite	piercing	10	1	10	10
226	139	Bite	piercing	7	1	6	6
227	140	Bite	piercing	33	4	12	12
228	140	Tail	bludgeoning	20	3	8	8
229	141	Bite	piercing	16	2	10	10
230	141	Claw	slashing	12	2	6	6
231	142	Bite	piercing	15	2	10	10
232	142	Claw	slashing	11	2	6	6
233	143	Claw	slashing	8	1	8	8
234	143	Sting	piercing	13	2	8	8
235	144	Slam	bludgeoning	16	2	10	10
236	145	Morningstar	piercing	21	3	8	8
237	145	Rock	bludgeoning	30	4	10	10
238	146	Greatsword	slashing	28	6	6	6
239	146	Rock	bludgeoning	29	4	10	10
240	147	Pincer	bludgeoning	16	2	10	10
241	147	Fist	bludgeoning	7	2	4	4
242	148	Slam	bludgeoning	16	3	6	6
243	148	Rock	bludgeoning	28	4	10	10
244	149	Bite	piercing	16	2	10	10
245	149	Claw	slashing	12	2	6	6
246	150	Bite	piercing	17	2	10	10
247	150	Claw	slashing	13	2	6	6
248	151	Tentacle	bludgeoning	12	2	6	6
249	151	Tail	bludgeoning	15	3	6	6
250	152	Mace	bludgeoning	7	1	6	6
251	153	Bite	piercing	8	1	8	8
252	154	Slam	bludgeoning	19	3	8	8
253	155	Bite	piercing	17	2	10	10
254	155	Claw	slashing	13	2	6	6
255	156	Bite	piercing	17	2	10	10
256	156	Claw	slashing	13	2	6	6
257	157	Bite	piercing	22	3	10	10
258	157	Constrict	bludgeoning	17	2	10	10
259	158	Scimitar	slashing	12	2	6	6
260	159	Scimitar	slashing	13	2	6	6
261	160	Claw	slashing	13	2	8	8
262	161	Fork	piercing	15	2	8	8
263	161	Tail	piercing	10	1	8	8
264	162	Bite	piercing	40	6	10	10
265	163	Beak	piercing	27	4	8	8
266	163	Talons	slashing	23	4	6	6
267	164	Longsword	slashing	8	1	8	8
268	164	Longbow	piercing	7	1	8	8
269	165	Bite	piercing	17	2	10	10
270	165	Claw	slashing	13	2	6	6
271	165	Tail	bludgeoning	15	2	8	8
272	166	Bite	piercing	17	2	10	10
273	166	Claw	slashing	13	2	6	6
274	166	Tail	bludgeoning	15	2	8	8
275	167	Bite	piercing	32	5	10	10
276	167	Claw	slashing	15	3	6	6
277	168	Claw	slashing	9	2	6	6
278	169	Greatsword	slashing	30	6	6	6
279	169	Rock	bludgeoning	35	4	12	12
280	170	Unarmed	bludgeoning	8	1	8	8
281	170	Bite	piercing	7	1	6	6
282	171	Bite	piercing	17	2	10	10
283	171	Claw	slashing	13	2	6	6
284	171	Tail	bludgeoning	15	2	8	8
285	172	Bite	piercing	17	2	10	10
286	172	Claw	slashing	13	2	6	6
287	172	Tail	bludgeoning	15	2	8	8
288	173	Bite	piercing	12	2	6	6
289	173	Claws	slashing	10	2	4	4
290	173	Tail	bludgeoning	12	2	6	6
291	174	Bite	piercing	18	2	10	10
292	174	Claw	slashing	14	2	6	6
293	174	Tail	bludgeoning	16	2	8	8
294	175	Bite	piercing	17	2	10	10
295	175	Claw	slashing	13	2	6	6
296	175	Tail	bludgeoning	15	2	8	8
297	176	Rotting	bludgeoning	14	3	6	6
298	177	Bite	piercing	22	3	8	8
299	177	Stinger	piercing	19	3	6	6
300	178	Bite	piercing	18	2	10	10
301	178	Claw	slashing	14	2	6	6
302	178	Tail	bludgeoning	16	2	8	8
303	179	Bite	piercing	19	2	10	10
304	179	Claw	slashing	15	2	6	6
305	179	Tail	bludgeoning	17	2	8	8
306	180	Slam	bludgeoning	20	3	8	8
307	180	Sword	slashing	23	3	10	10
308	181	Longsword	slashing	13	2	8	8
309	181	Tail	bludgeoning	15	2	10	10
310	182	Greatsword	slashing	21	4	6	6
311	183	Bite	piercing	19	2	10	10
312	183	Claw	slashing	15	2	6	6
313	183	Tail	bludgeoning	17	2	8	8
314	184	Bite	piercing	19	2	10	10
315	184	Claw	slashing	15	2	6	6
316	184	Tail	bludgeoning	17	2	8	8
317	185	Claw	slashing	17	2	10	10
318	186	Bite	piercing	26	3	12	12
319	186	Claw	slashing	16	2	8	8
320	186	Tail	bludgeoning	26	3	12	12
321	187	Longsword	slashing	21	3	8	8
322	187	Whip	slashing	15	2	6	6
323	188	Bite	piercing	19	2	10	10
324	188	Claw	slashing	15	2	6	6
325	188	Tail	bludgeoning	17	2	8	8
326	189	Bite	piercing	19	2	10	10
327	189	Claw	slashing	15	2	6	6
328	189	Tail	bludgeoning	17	2	8	8
329	190	Bite	piercing	22	4	6	6
330	190	Claw	slashing	17	2	8	8
331	190	Mace	bludgeoning	15	2	6	6
332	190	Tail	bludgeoning	24	3	10	10
\.


--
-- Name: attacks_attack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('attacks_attack_id_seq', 332, true);


--
-- Data for Name: friendships; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY friendships (friendship_id, user_id_1, user_id_2, verified) FROM stdin;
1	1	2	t
2	1	2	t
\.


--
-- Name: friendships_friendship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('friendships_friendship_id_seq', 2, true);


--
-- Data for Name: goals; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY goals (goal_id, user_id, goal_type, valid_from, valid_to, value, xp, frequency, resolved) FROM stdin;
2	2	Steps	2017-10-01 00:00:00	2017-10-10 00:00:00	7000	300	Daily	\N
1	1	Steps	2017-09-19 00:00:00	2017-09-25 00:00:00	15000	300	\N	Y
\.


--
-- Name: goals_goal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('goals_goal_id_seq', 2, true);


--
-- Data for Name: goalstatuses; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY goalstatuses (goalstatus_id, goal_id, date_recorded, value) FROM stdin;
1	1	2017-09-24 00:00:00	1000
2	2	2017-10-03 00:00:00	1000
3	1	2017-10-05 17:15:10.643375	97637
4	2	2017-10-05 21:10:29.62774	5291
\.


--
-- Name: goalstatuses_goalstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('goalstatuses_goalstatus_id_seq', 4, true);


--
-- Data for Name: levellookup; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY levellookup (level, min_cr, max_cr, required_xp, hit_point_max) FROM stdin;
1	0	0.25	0	8
2	0.25	0.5	300	12
3	0.5	0.75	900	16
4	0.75	1	2700	20
5	1	1.25	6500	24
6	1.25	1.5	14000	28
7	1.5	1.75	23000	32
8	1.75	2	34000	36
9	2	2.25	48000	40
10	2.25	2.5	64000	44
11	2.5	2.75	85000	48
12	2.75	3	100000	52
13	3	3.25	120000	56
14	3.25	3.5	140000	60
15	3.5	3.75	165000	64
16	3.75	4	195000	68
17	4	4.25	225000	72
18	4.25	4.5	265000	76
19	4.5	4.75	305000	80
20	4.75	5	355000	84
\.


--
-- Name: levellookup_level_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('levellookup_level_seq', 1, false);


--
-- Data for Name: monsters; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY monsters (monster_id, name, cr) FROM stdin;
0	Kobold	0.125
1	Merfolk	0.125
2	Stirge	0.125
3	Aarakocra	0.25
4	Bullywug	0.25
5	Dretch	0.25
6	Drow	0.25
7	Flying Sword	0.25
8	Goblin	0.25
9	Grimlock	0.25
10	Pseudodragon	0.25
11	Pteranodon	0.25
12	Skeleton	0.25
13	Sprite	0.25
14	Steam Mephit	0.25
15	Violet Fungus	0.25
16	Zombie	0.25
17	Cockatrice	0.5
18	Darkmantle	0.5
19	Dust Mephit	0.5
20	Gnoll	0.5
21	Deep Gnome (Svirfneblin)	0.5
22	Gray Ooze	0.5
23	Hobgoblin	0.5
24	Ice Mephit	0.5
25	Lizardfolk	0.5
26	Magma Mephit	0.5
27	Magmin	0.5
28	Orc	0.5
29	Rust Monster	0.5
30	Sahuagin	0.5
31	Satyr	0.5
32	Shadow	0.5
33	Warhorse Skeleton	0.5
34	Animated Armor	1
35	Brass Dragon Wyrmling	1
36	Bugbear	1
37	Copper Dragon Wyrmling	1
38	Dryad	1
39	Duergar	1
40	Ghoul	1
41	Harpy	1
42	Hippogriff	1
43	Imp	1
44	Quasit	1
45	Specter	1
46	Allosaurus	2
47	Ankheg	2
48	Azer	2
49	Black Dragon Wyrmling	2
50	Bronze Dragon Wyrmling	2
51	Centaur	2
52	Ettercap	2
53	Gargoyle	2
54	Gelatinous Cube	2
55	Ghast	2
56	Gibbering Mouther	2
57	Green Dragon Wyrmling	2
58	Grick	2
59	Griffon	2
60	Merrow	2
61	Mimic	2
62	Minotaur Skeleton	2
63	Ochre Jelly	2
64	Ogre	2
65	Ogre Zombie	2
66	Pegasus	2
67	Plesiosaurus	2
68	Rug of Smothering	2
69	Sea Hag	2
70	Silver Dragon Wyrmling	2
71	Wererat	2
72	White Dragon Wyrmling	2
73	Will-o'-Wisp	2
74	Ankylosaurus	3
75	Basilisk	3
76	Bearded Devil	3
77	Blue Dragon Wyrmling	3
78	Doppelganger	3
79	Gold Dragon Wyrmling	3
80	Green Hag	3
81	Hell Hound	3
82	Manticore	3
83	Minotaur	3
84	Mummy	3
85	Nightmare	3
86	Owlbear	3
87	Werewolf	3
88	Wight	3
89	Black Pudding	4
90	Chuul	4
91	Couatl	4
92	Ettin	4
93	Ghost	4
94	Lamia	4
95	Red Dragon Wyrmling	4
96	Succubus/Incubus	4
97	Wereboar	4
98	Weretiger	4
99	Air Elemental	5
100	Barbed Devil	5
101	Bulette	5
102	Earth Elemental	5
103	Fire Elemental	5
104	Flesh Golem	5
105	Gorgon	5
106	Half-Red Dragon Veteran	5
107	Hill Giant	5
108	Night Hag	5
109	Otyugh	5
110	Roper	5
111	Salamander	5
112	Shambling Mound	5
113	Triceratops	5
114	Troll	5
115	Contents	5
116	Vampire Spawn	5
117	Water Elemental	5
118	Werebear	5
119	Wraith	5
120	Xorn	5
121	Chimera	6
122	Drider	6
123	Invisible Stalker	6
124	Medusa	6
125	Vrock	6
126	Wyvern	6
127	Young Brass Dragon	6
128	Young White Dragon	6
129	Oni	7
130	Shield Guardian	7
131	Stone Giant	7
132	Young Black Dragon	7
133	Young Copper Dragon	7
134	Chain Devil	8
135	Cloaker	8
136	Frost Giant	8
137	Hezrou	8
138	Hydra	8
139	Spirit Naga	8
140	Tyrannosaurus Rex	8
141	Young Bronze Dragon	8
142	Young Green Dragon	8
143	Bone Devil	9
144	Clay Golem	9
145	Cloud Giant	9
146	Fire Giant	9
147	Glabrezu	9
148	Treant	9
149	Young Blue Dragon	9
150	Young Silver Dragon	9
151	Aboleth	10
152	Deva	10
153	Guardian Naga	10
154	Stone Golem	10
155	Young Gold Dragon	10
156	Young Red Dragon	10
157	Behir	11
158	Djinni	11
159	Efreeti	11
160	Contents	11
161	Horned Devil	11
162	Remorhaz	11
163	Roc	11
164	Erinyes	12
165	Adult Brass Dragon	13
166	Adult White Dragon	13
167	Nalfeshnee	13
168	Rakshasa	13
169	Storm Giant	13
170	Contents	13
171	Adult Black Dragon	14
172	Adult Copper Dragon	14
173	Ice Devil	14
174	Adult Bronze Dragon	15
175	Adult Green Dragon	15
176	Contents	15
177	Purple Worm	15
178	Adult Blue Dragon	16
179	Adult Silver Dragon	16
180	Iron Golem	16
181	Marilith	16
182	Planetar	16
183	Adult Gold Dragon	17
184	Adult Red Dragon	17
185	Contents	17
186	Dragon Turtle	17
187	Balor	19
188	Ancient Brass Dragon	20
189	Ancient White Dragon	20
190	Pit Fiend	20
\.


--
-- Name: monsters_monster_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('monsters_monster_id_seq', 1, false);


--
-- Data for Name: sleepstatuses; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY sleepstatuses (goalstatus_id, bedtime, waketime) FROM stdin;
\.


--
-- Data for Name: teams; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY teams (team_id, teamname) FROM stdin;
\.


--
-- Name: teams_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('teams_team_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY users (user_id, username, email, password) FROM stdin;
1	ToK	sarahjaneiom@gmail.com	1234
2	Gundren	gundren@rockseeker.com	1111
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('users_user_id_seq', 2, true);


--
-- Data for Name: userstatuses; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY userstatuses (userstatus_id, user_id, level, current_xp, current_hp, date_recorded) FROM stdin;
1	1	1	0	12	2017-09-24 00:00:00
2	2	1	0	12	2017-10-03 00:00:00
3	1	2	300	12	2017-10-05 17:15:14.6943
\.


--
-- Name: userstatuses_userstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('userstatuses_userstatus_id_seq', 3, true);


--
-- Data for Name: userteams; Type: TABLE DATA; Schema: public; Owner: sarah
--

COPY userteams (userteam_id, team_id, user_id, valid_from, valid_to) FROM stdin;
\.


--
-- Name: userteams_userteam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sarah
--

SELECT pg_catalog.setval('userteams_userteam_id_seq', 1, false);


--
-- Name: attacks_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY attacks
    ADD CONSTRAINT attacks_pkey PRIMARY KEY (attack_id);


--
-- Name: friendships_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY friendships
    ADD CONSTRAINT friendships_pkey PRIMARY KEY (friendship_id);


--
-- Name: goals_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY goals
    ADD CONSTRAINT goals_pkey PRIMARY KEY (goal_id);


--
-- Name: goalstatuses_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY goalstatuses
    ADD CONSTRAINT goalstatuses_pkey PRIMARY KEY (goalstatus_id);


--
-- Name: levellookup_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY levellookup
    ADD CONSTRAINT levellookup_pkey PRIMARY KEY (level);


--
-- Name: monsters_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY monsters
    ADD CONSTRAINT monsters_pkey PRIMARY KEY (monster_id);


--
-- Name: sleepstatuses_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY sleepstatuses
    ADD CONSTRAINT sleepstatuses_pkey PRIMARY KEY (goalstatus_id);


--
-- Name: teams_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (team_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: userstatuses_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY userstatuses
    ADD CONSTRAINT userstatuses_pkey PRIMARY KEY (userstatus_id);


--
-- Name: userteams_pkey; Type: CONSTRAINT; Schema: public; Owner: sarah; Tablespace: 
--

ALTER TABLE ONLY userteams
    ADD CONSTRAINT userteams_pkey PRIMARY KEY (userteam_id);


--
-- Name: attacks_monster_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY attacks
    ADD CONSTRAINT attacks_monster_id_fkey FOREIGN KEY (monster_id) REFERENCES monsters(monster_id);


--
-- Name: friendships_user_id_1_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY friendships
    ADD CONSTRAINT friendships_user_id_1_fkey FOREIGN KEY (user_id_1) REFERENCES users(user_id);


--
-- Name: friendships_user_id_2_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY friendships
    ADD CONSTRAINT friendships_user_id_2_fkey FOREIGN KEY (user_id_2) REFERENCES users(user_id);


--
-- Name: goals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY goals
    ADD CONSTRAINT goals_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: goalstatuses_goal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY goalstatuses
    ADD CONSTRAINT goalstatuses_goal_id_fkey FOREIGN KEY (goal_id) REFERENCES goals(goal_id);


--
-- Name: sleepstatuses_goalstatus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY sleepstatuses
    ADD CONSTRAINT sleepstatuses_goalstatus_id_fkey FOREIGN KEY (goalstatus_id) REFERENCES goalstatuses(goalstatus_id);


--
-- Name: userstatuses_level_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY userstatuses
    ADD CONSTRAINT userstatuses_level_fkey FOREIGN KEY (level) REFERENCES levellookup(level);


--
-- Name: userstatuses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY userstatuses
    ADD CONSTRAINT userstatuses_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: userteams_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY userteams
    ADD CONSTRAINT userteams_team_id_fkey FOREIGN KEY (team_id) REFERENCES teams(team_id);


--
-- Name: userteams_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sarah
--

ALTER TABLE ONLY userteams
    ADD CONSTRAINT userteams_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

