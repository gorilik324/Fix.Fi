// supabase.js
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://tlzdgevojpvplmjxfufr.supabase.co";
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRsemRnZXZvanB2cGxtanhmdWZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgxNTU3MTMsImV4cCI6MTk5MzczMTcxM30.qEO7kWnMn93hjVSm3opkSZ5a2BDS48ef34cc4RgkCz8';

export const supabase = createClient(supabaseUrl, supabaseKey);