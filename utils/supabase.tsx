// supabase.js
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://aufxkitkqmttoqylyqdh.supabase.co";
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1ZnhraXRrcW10dG9xeWx5cWRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njg5ODg0MDEsImV4cCI6MTk4NDU2NDQwMX0.YQF6yCaRgyLXiYebb--4fOH5u7MC2015M0prURZJ6hc';

export const supabase = createClient(supabaseUrl, supabaseKey);