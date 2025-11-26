import time
import sys
from src.logger_config import setup_logger
from src.scraper import get_links
from src.embeddings import get_embedding, get_embeddings
from src.similarity import find_closest
from src.stats import save_run, get_average_time

# Setup main logger
logger = setup_logger("Main")

def main():
    print("Welcome to Wikipedia Speedrunner (Python Edition)!")
    print("--------------------------------------------------")
    
    start_url = input("Enter Start Wikipedia URL (or term): ").strip()
    end_url = input("Enter End Wikipedia URL (or term): ").strip()
    
    # Basic handling if user enters just a term instead of full URL
    if not start_url.startswith("http"):
        start_url = f"https://en.wikipedia.org/wiki/{start_url.replace(' ', '_')}"
    if not end_url.startswith("http"):
        end_url = f"https://en.wikipedia.org/wiki/{end_url.replace(' ', '_')}"

    print(f"\nGoal: {start_url} -> {end_url}")
    print("Initializing models... (this may take a moment on first run)")
    
    # Pre-load model to avoid delay during loop
    try:
        # We need the embedding of the target to compare against
        # Extract the title/term from the end URL for embedding
        end_term = end_url.split("/wiki/")[-1].replace("_", " ")
        target_embedding = get_embedding(end_term)
        if target_embedding is None:
            print("Error: Could not generate embedding for target. Exiting.")
            return
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        print("Failed to initialize models. Check logs.")
        return

    current_url = start_url
    path = [current_url]
    start_time = time.time()
    visited = set()
    
    step_count = 0
    max_steps = 50 # Safety break
    
    while step_count < max_steps:
        step_count += 1
        print(f"\n[Step {step_count}] Current Page: {current_url}")
        logger.info(f"Step {step_count}: Visiting {current_url}")
        
        if current_url == end_url:
            print("\n>>> TARGET REACHED! <<<")
            break
            
        visited.add(current_url)
        
        # 1. Scrape links
        print("Scraping links...")
        links = get_links(current_url)
        
        if not links:
            print("Dead end! No links found.")
            logger.warning(f"Dead end at {current_url}")
            break
            
        # 2. Check for direct match
        # We check if any link matches the end_url
        found_direct = False
        for title, url in links:
            if url == end_url:
                print(f"Found direct link to target: {title}")
                current_url = url
                path.append(current_url)
                found_direct = True
                break
        
        if found_direct:
            continue

        # 3. Calculate embeddings for candidates
        # Optimization: Filter out already visited links to avoid loops
        candidates = []
        candidate_texts = []
        
        for title, url in links:
            if url not in visited:
                candidates.append((title, url))
                candidate_texts.append(title)
        
        if not candidates:
            print("All links on this page have been visited. Backtracking not implemented.")
            logger.warning("All links visited.")
            break

        print(f"Analyzing {len(candidates)} links...")
        
        # Batch embedding generation is faster
        candidate_embeddings = get_embeddings(candidate_texts)
        
        if len(candidate_embeddings) != len(candidates):
            logger.error("Mismatch in embeddings count.")
            break
            
        # Re-structure for similarity function: (title, url, embedding)
        candidates_with_embeddings = []
        for i in range(len(candidates)):
            candidates_with_embeddings.append((candidates[i][0], candidates[i][1], candidate_embeddings[i]))
            
        # 4. Find closest
        best_title, best_url = find_closest(target_embedding, candidates_with_embeddings)
        
        if best_url:
            print(f"Best link: {best_title}")
            current_url = best_url
            path.append(current_url)
        else:
            print("Could not determine best link.")
            break
            
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n--------------------------------------------------")
    print(f"Run Complete!")
    print(f"Total Steps: {len(path)}")
    print(f"Time Taken: {duration:.2f} seconds")
    print(f"Path: {' -> '.join(path)}")
    
    save_run(start_url, end_url, path, duration)
    
    avg_time = get_average_time()
    print(f"Average Run Time (All Runs): {avg_time:.2f} seconds")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
