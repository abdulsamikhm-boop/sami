import asyncio
import time

async def mock_llm_stream(prompt: str):
    print(f"🤖 Starting LLM stream for: '{prompt}'")
    for i in range(1, 6):
        await asyncio.sleep(0.5) 
        yield f"Token {i} "

async def background_task():
    for i in range(1, 4):
        await asyncio.sleep(0.4)
        print(f"⚙️ Background task heartbeat {i}")

async def main():
    start_time = time.time()
    
    bg_task = asyncio.create_task(background_task())
    
    prompt = "Explain quantum computing in one sentence."
    async for token in mock_llm_stream(prompt):
        print(token, end="", flush=True)
    print("\n✨ LLM streaming complete.")
    
    await bg_task
    
    end_time = time.time()
    print(f"⏱️ Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
