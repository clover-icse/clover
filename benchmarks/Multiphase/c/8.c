int main(){
    int x, y;

    // pre-conditions
    x = 1;
    y = 0;

    // loop body
    while(unknown()){
        if(x % 2 == 0){
            y = y + 1;
        }
        x = x + 1;
        
    }

    // post-condition
    if(x == (2 * 1351235)){
        assert(y == 1351234);
    }
    
}