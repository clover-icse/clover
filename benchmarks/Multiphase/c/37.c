int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    y = 0;
    z = 0;
    

    // loop body
    while(unknown()){
        if(x == 0){
            y = 523;
        }else{
            y = y + z;
            z = 250;
        }
        x = x + 1;
        
    }

    // post-condition
    if(x >= 10){
        assert(y > 2500);
    }
    
}