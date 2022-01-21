const buildChain = (blocks) => {
  const index = new Map(blocks.map(b => ([b.hash, b])));
  const result = {};
  blocks.forEach(block => {
    const key = block.__type;
    if (key) {
      block.__prev = null;
      
      if (block['previous_hash']) {
        block.__prev = index.get(block['previous_hash']);
      }

      result[key] = block;
    }
  });
  return result;
};

export default buildChain;