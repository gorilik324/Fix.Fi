import { supabase } from "../../../utils/supabase"

export default async function handler(req, res) {

  const {address} = req.query

  let { data, error } = await supabase
  .from('Null_Balances')
  .select()
  .filter('ADDRESS', 'eq', address)
  
  res.status(200).json(data)
if (error) console.log(error)
}
