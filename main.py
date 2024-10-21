from api.LLMCoder import LLMCoder
from api.LLMPlanner import LLMPlanner
from api.LLMSummarizer import LLMSummarizer
from LLM.call_llm_api.call_llm import main_logger
import os

def pipeline():


    os.popen('rm -rf res-*')
    os.popen('rm -rf *.log')
    planner = LLMPlanner()

    plan_times = 10
    generate_times = 5

    
    promotion = ''
    result = None
    # Overall 50 rounds.
    for plan_idx in range(plan_times):

        main_logger.info('---------------------Planning---------------------')
        print('---------------------Planning---------------------')

        tactics = planner.plan(result)
        print(tactics)

        
        coder = LLMCoder()
        # Generate code 5 rounds.
        for iter_idx in range(generate_times):

            main_logger.info('##################### Generating #####################')
            print('##################### Generating #####################')

            code = coder.generate_code(tactics, promotion)
            if code == None:
                main_logger.debug('The on_step function defination is wrong. Re-generate the code.')
                print('The on_step function defination is wrong. Re-generate the code.')
                promotion += 'Please define the function as def async on_step(self, iteration: int)'
                continue
            print(code)
            data = coder.test_code(plan_idx, iter_idx)
            if data['type'] == 'bug':
                # TODO
                result = data['message']
            else:
                result = data['message']
                if result['win'] == result['times']:
                    
                    main_logger.debug('Achieve Winning results, process terminated')
                    print('Achieve Winning results, process terminated')
                    return
                
            main_logger.info('!!!!!!!!!!!!!!!!!!!!! Summarizing !!!!!!!!!!!!!!!!!!!!!')
            print('!!!!!!!!!!!!!!!!!!!!! Summarizing !!!!!!!!!!!!!!!!!!!!!')
            
            if iter_idx != generate_times -1 :
                summarizer = LLMSummarizer()
                promotion = summarizer.summarize(code, result)
                print(promotion)

                if '[Change Tactic]' in promotion:
                    break

        
        if type(result) == dict:
            tactic_name = planner.retrival_information(tactics)
            for t in tactic_name:
                planner.update_history(t, result['win']/result['times'])

if __name__ == '__main__':
    
    pipeline()
    

    
