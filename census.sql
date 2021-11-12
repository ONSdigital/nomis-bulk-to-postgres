--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4 (Debian 13.4-0+deb11u1)
-- Dumped by pg_dump version 13.4 (Debian 13.4-0+deb11u1)

-- ... and modified by hand!

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE census;
--
-- Name: census; Type: DATABASE; Schema: -; Owner: census
--

CREATE DATABASE census WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_GB.UTF-8';


ALTER DATABASE census OWNER TO census;

\connect census

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--- --
--- -- Name: nomis_category; Type: TABLE; Schema: public; Owner: census
--- --
--- 
--- CREATE TABLE public.nomis_category (
---     id integer NOT NULL,
---     nomis_desc_id integer,
---     category_name text,
---     measurement_unit text,
---     stat_unit text,
---     long_nomis_code text,
---     year integer
--- );
--- 
--- 
--- ALTER TABLE public.nomis_category OWNER TO census;
--- 
--- --
--- -- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: census
--- --
--- 
--- CREATE SEQUENCE public.categories_category_id_seq
---     AS integer
---     START WITH 1
---     INCREMENT BY 1
---     NO MINVALUE
---     NO MAXVALUE
---     CACHE 1;
--- 
--- 
--- ALTER TABLE public.categories_category_id_seq OWNER TO census;
--- 
--- --
--- -- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: census
--- --
--- 
--- ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.nomis_category.id;
--- 
--- 
--- --
--- -- Name: geo_metric; Type: TABLE; Schema: public; Owner: census
--- --
--- 
--- CREATE TABLE public.geo_metric (
---     id integer NOT NULL,
---     geo_id integer,
---     year integer,
---     category_id integer,
---     metric double precision
--- );
--- 
--- 
--- ALTER TABLE public.geo_metric OWNER TO census;
--- 
--- --
--- -- Name: counts_count_id_seq; Type: SEQUENCE; Schema: public; Owner: census
--- --
--- 
--- CREATE SEQUENCE public.counts_count_id_seq
---     AS integer
---     START WITH 1
---     INCREMENT BY 1
---     NO MINVALUE
---     NO MAXVALUE
---     CACHE 1;
--- 
--- 
--- ALTER TABLE public.counts_count_id_seq OWNER TO census;
--- 
--- --
--- -- Name: counts_count_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: census
--- --
--- 
--- ALTER SEQUENCE public.counts_count_id_seq OWNED BY public.geo_metric.id;
--- 
--- 
--- --
--- -- Name: geo; Type: TABLE; Schema: public; Owner: census
--- --
--- 
--- CREATE TABLE public.geo (
---     id integer NOT NULL,
---     geo_code text,
---     geo_name text,
---     geo_type_id integer
--- );
--- 
--- 
--- ALTER TABLE public.geo OWNER TO census;
--- 
--- --
--- -- Name: geo_id_seq; Type: SEQUENCE; Schema: public; Owner: census
--- --
--- 
--- CREATE SEQUENCE public.geo_id_seq
---     START WITH 1
---     INCREMENT BY 1
---     NO MINVALUE
---     NO MAXVALUE
---     CACHE 1;
--- 
--- 
--- ALTER TABLE public.geo_id_seq OWNER TO census;
--- 
--- --
--- -- Name: geo_type; Type: TABLE; Schema: public; Owner: census
--- --
--- 
--- CREATE TABLE public.geo_type (
---     id integer NOT NULL,
---     geo_type_name text
--- );
--- 
--- 
--- ALTER TABLE public.geo_type OWNER TO census;
--- 
--- --
--- -- Name: lsoa2011_lad2020_lookup; Type: TABLE; Schema: public; Owner: census
--- --
--- 
--- CREATE TABLE public.lsoa2011_lad2020_lookup (
---     id integer NOT NULL,
---     lsoa2011code text,
---     lad2020code text
--- );
--- 
--- 
--- ALTER TABLE public.lsoa2011_lad2020_lookup OWNER TO census;
--- 
--- --
--- -- Name: lsoa2011_lad2020_lookup_id_seq; Type: SEQUENCE; Schema: public; Owner: census
--- --
--- 
--- CREATE SEQUENCE public.lsoa2011_lad2020_lookup_id_seq
---     AS integer
---     START WITH 1
---     INCREMENT BY 1
---     NO MINVALUE
---     NO MAXVALUE
---     CACHE 1;
--- 
--- 
--- ALTER TABLE public.lsoa2011_lad2020_lookup_id_seq OWNER TO census;
--- 
--- --
--- -- Name: lsoa2011_lad2020_lookup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: census
--- --
--- 
--- ALTER SEQUENCE public.lsoa2011_lad2020_lookup_id_seq OWNED BY public.lsoa2011_lad2020_lookup.id;
--- 
--- 
--- --
--- -- Name: nomis_desc; Type: TABLE; Schema: public; Owner: census
--- --
--- 
--- CREATE TABLE public.nomis_desc (
---     id integer NOT NULL,
---     short_desc text,
---     long_desc text,
---     short_nomis_code text,
---     year integer
--- );
--- 
--- 
--- ALTER TABLE public.nomis_desc OWNER TO census;
--- 
--- --
--- -- Name: variables_var_id_seq; Type: SEQUENCE; Schema: public; Owner: census
--- --
--- 
--- CREATE SEQUENCE public.variables_var_id_seq
---     AS integer
---     START WITH 1
---     INCREMENT BY 1
---     NO MINVALUE
---     NO MAXVALUE
---     CACHE 1;
--- 
--- 
--- ALTER TABLE public.variables_var_id_seq OWNER TO census;
--- 
--- --
--- -- Name: variables_var_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: census
--- --
--- 
--- ALTER SEQUENCE public.variables_var_id_seq OWNED BY public.nomis_desc.id;
--- 
--- 
--- --
--- -- Name: geo_metric id; Type: DEFAULT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.geo_metric ALTER COLUMN id SET DEFAULT nextval('public.counts_count_id_seq'::regclass);
--- 
--- 
--- --
--- -- Name: lsoa2011_lad2020_lookup id; Type: DEFAULT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.lsoa2011_lad2020_lookup ALTER COLUMN id SET DEFAULT nextval('public.lsoa2011_lad2020_lookup_id_seq'::regclass);
--- 
--- 
--- --
--- -- Name: nomis_category id; Type: DEFAULT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.nomis_category ALTER COLUMN id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);
--- 
--- 
--- --
--- -- Name: nomis_desc id; Type: DEFAULT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.nomis_desc ALTER COLUMN id SET DEFAULT nextval('public.variables_var_id_seq'::regclass);
--- 
--- 
--- --
--- -- Name: nomis_category categories_pkey; Type: CONSTRAINT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.nomis_category
---     ADD CONSTRAINT categories_pkey PRIMARY KEY (id);
--- 
--- 
--- --
--- -- Name: geo_metric counts_pkey; Type: CONSTRAINT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.geo_metric
---     ADD CONSTRAINT counts_pkey PRIMARY KEY (id);
--- 
--- 
--- --
--- -- Name: lsoa2011_lad2020_lookup lsoa2011_lad2020_lookup_pkey; Type: CONSTRAINT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.lsoa2011_lad2020_lookup
---     ADD CONSTRAINT lsoa2011_lad2020_lookup_pkey PRIMARY KEY (id);
--- 
--- 
--- --
--- -- Name: geo_type place_types_pkey; Type: CONSTRAINT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.geo_type
---     ADD CONSTRAINT place_types_pkey PRIMARY KEY (id);
--- 
--- 
--- --
--- -- Name: geo places_pkey; Type: CONSTRAINT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.geo
---     ADD CONSTRAINT places_pkey PRIMARY KEY (id);
--- 
--- 
--- --
--- -- Name: nomis_desc variables_pkey; Type: CONSTRAINT; Schema: public; Owner: census
--- --
--- 
--- ALTER TABLE ONLY public.nomis_desc
---     ADD CONSTRAINT variables_pkey PRIMARY KEY (id);

CREATE TABLE IF NOT EXISTS public.geo_metric(
        id SERIAL PRIMARY KEY,
        geo_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        metric INTEGER NOT NULL
    );
CREATE TABLE IF NOT EXISTS public.nomis_desc(
        id SERIAL PRIMARY KEY NOT NULL,
        short_desc TEXT NOT NULL,
        long_desc TEXT NOT NULL,
        short_nomis_code TEXT NOT NULL,
        year INTEGER NOT NULL
    );
CREATE TABLE IF NOT EXISTS public.nomis_category(
        id SERIAL PRIMARY KEY,
        nomis_desc_id INTEGER NOT NULL,
        category_name TEXT NOT NULL,
        measurement_unit TEXT NOT NULL,
        stat_unit TEXT NOT NULL,
        long_nomis_code TEXT NOT NULL,
        year INTEGER NOT NULL
    );
CREATE TABLE IF NOT EXISTS public.LSOA2011_LAD2020_LOOKUP(
        id SERIAL PRIMARY KEY,
        lsoa2011code TEXT NOT NULL,
        lad2020code TEXT NOT NULL
    );
CREATE TABLE IF NOT EXISTS public.geo_type(
        id INTEGER PRIMARY KEY,
        geo_type_name TEXT NOT NULL
    );
CREATE TABLE IF NOT EXISTS public.geo(
        id SERIAL PRIMARY KEY,
        geo_code TEXT NOT NULL,
        geo_name TEXT NOT NULL,
        geo_type_id INTEGER NOT NULL
    );

--
-- Name: idx_counts_category_id; Type: INDEX; Schema: public; Owner: census
--

CREATE INDEX idx_counts_category_id ON public.geo_metric USING btree (category_id);


--
-- Name: idx_counts_geo_code; Type: INDEX; Schema: public; Owner: census
--

CREATE INDEX idx_counts_geo_code ON public.geo_metric USING btree (geo_id);


--
-- Name: geo_metric fk_geo; Type: FK CONSTRAINT; Schema: public; Owner: census
--

ALTER TABLE ONLY public.geo_metric
    ADD CONSTRAINT fk_geo FOREIGN KEY (geo_id) REFERENCES public.geo(id);


--
-- Name: geo fk_geo_type; Type: FK CONSTRAINT; Schema: public; Owner: census
--

ALTER TABLE ONLY public.geo
    ADD CONSTRAINT fk_geo_type FOREIGN KEY (geo_type_id) REFERENCES public.geo_type(id);


--
-- Name: geo_metric fk_nomis_category; Type: FK CONSTRAINT; Schema: public; Owner: census
--

ALTER TABLE ONLY public.geo_metric
    ADD CONSTRAINT fk_nomis_category FOREIGN KEY (category_id) REFERENCES public.nomis_category(id);


--
-- Name: nomis_category fk_nomis_desc; Type: FK CONSTRAINT; Schema: public; Owner: census
--

ALTER TABLE ONLY public.nomis_category
    ADD CONSTRAINT fk_nomis_desc FOREIGN KEY (nomis_desc_id) REFERENCES public.nomis_desc(id);


--
-- PostgreSQL database dump complete
--

